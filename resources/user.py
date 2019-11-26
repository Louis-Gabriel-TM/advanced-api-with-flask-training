from typing import Tuple

from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required
)
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST


USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."


user_schema = UserSchema()  # this Schema has notably deprecated the json() method


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
            # dump() serializes: object -> dict
            return user_schema.dump(user), 200

        return {'message': USER_NOT_FOUND}, 404

    @classmethod
    def delete(cls, user_id: int) -> Tuple:
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
            return {'message': USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls) -> Tuple:
        user_json = request.get_json()
        # load() deserializes: dict -> object
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)

        # safe_str_cmp to avoid byte strings
        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200

        return {'message': INVALID_CREDENTIALS}, 401


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls) -> Tuple:
        # 'jti' for 'JWT ID', a unique identifier for a token
        jti = get_raw_jwt()['jti']
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)

        return {'message': USER_LOGGED_OUT.format(user_id)}, 200


class UserRegister(Resource):

    @classmethod
    def post(cls) -> Tuple:
        user_json = request.get_json()
        # load() deserializes: dict -> object
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.password):
            return {'message': USER_ALREADY_EXISTS}, 400

        user.save_to_db()  # password should be encrypted before saving

        return {'message': CREATED_SUCCESSFULLY}, 201


class TokenRefresh(Resource):

    @classmethod
    @jwt_refresh_token_required
    def post(cls) -> Tuple:
        """
        Get a new access token without requiring username and password,
        but only the 'refresh token' provided during login.
        The refreshed access token has a 'fresh=False' argument which means
        the user may have not given username and password for a long time.
        """

        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': new_token}, 200
