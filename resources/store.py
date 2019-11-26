from typing import Tuple

from flask_restful import Resource

from models.store import StoreModel
from schemas.store import StoreSchema


ERROR_INSERTING = "An error occurred while inserting the store."
NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
STORE_DELETED = "Store deleted."
STORE_NOT_FOUND = "Store not found."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):

    @classmethod
    def get(cls, name: str) -> Tuple:
        store = StoreModel.find_by_name(name)

        if store:
            return store_schema.dump(store), 200

        return {'message': STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str) -> Tuple:
        if StoreModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS}, 400

        # no more __init__() method so a mapping by keywords is necessary:
        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str) -> Tuple:
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
            return {'message': STORE_DELETED}, 200
        
        return {'message': STORE_NOT_FOUND}, 404


class StoreList(Resource):

    @classmethod
    def get(cls):
        return {
            'stores': store_list_schema.dump(StoreModel.find_all())
        }, 200
