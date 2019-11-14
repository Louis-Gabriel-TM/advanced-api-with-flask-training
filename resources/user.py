from typing import Tuple

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required
)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="This field cannot be blank."
)


class User(Resource):  # should be absent in production
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int) -> Tuple:
        user = UserModel.find_by_id(user_id)

        if user:
            return user.json(), 200

        return {'message': "User not found."}, 404

    @classmethod
    def delete(cls, user_id: int) -> Tuple:
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
            return {'message': "User deleted."}, 200


class UserLogin(Resource):
    
    def post(self) -> Tuple:
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):  # safe_str_cmp to avoid byte strings
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': "Invalid credentials."}, 401


class UserLogout(Resource):
    
    @jwt_required
    def post(self) -> Tuple:
        jti = get_raw_jwt()['jti']  # 'jti' for 'JWT ID', a unique identifier for a token
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)

        return {'message': f"User <id={user_id}> successfully logged out."}, 200


class UserRegister(Resource):
    
    def post(self) -> Tuple:
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()  # password should be encrypted before saving

        return {'message': "User created successfully."}, 201


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self) -> Tuple:
        """
        Get a new access token without requiring username and password,
        but only the 'refresh token' provided during login.
        The refreshed access token has a 'fresh=False' argument which means
        the user may have not given username and password for a long time.
        """

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': new_token}, 200
