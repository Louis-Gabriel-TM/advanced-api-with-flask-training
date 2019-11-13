from flask import Flask,jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import TokenRefresh, User, UserLogin, UserLogout, UserRegister


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # what database manager to use
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # tracking done by SQLAlchemy
app.config['PROPAGATE_EXCEPTIONS'] = True  # to see Flask-RESTful exceptions
app.config['JWT_BLACKLIST_ENABLED'] = True  # needed for allowing users to log out
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'My Very Secret Key'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader  # to add arbitrary informations in JWTokens
def add_claims_to_jwt(identity):  # 'identity' is defined at the token creation
    if identity == 1:  # should read admins list from a file or a database
        return {'is_admin': True}

    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # blacklist some previous tokens

# The following methods customize JWT response or errors
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': "The token has expired.",
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_call_back(error):
    return jsonify({
        'description': "Signature verification failed.",
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': "Request dos noy contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': "The token is nor fresh.",
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserRegister, '/user/register')


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
