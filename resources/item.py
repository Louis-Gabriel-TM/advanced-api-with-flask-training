from typing import Tuple

from flask_jwt_extended import (
    fresh_jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_required,
    jwt_optional
)
from flask_restful import Resource, reqparse

from models.item import ItemModel


ADMIN_REQUIRED = "Admin privileges required."
BLANK_ERROR = "{} cannot be left blank."
INSERTION_ERROR = "An error occured while inserting the item."
ITEM_ALREADY_EXISTS = "An item with name '{}' already exists."
ITEM_DELETED = "Item deleted."
ITEM_NOT_FOUND = "Item not found."
MORE_DATA = "More data available if you log in."


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help=BLANK_ERROR.format("'price'"),
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help=BLANK_ERROR.format("'store_id'"),
    )

    @classmethod
    def get(cls, name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str) -> Tuple:
        if ItemModel.find_by_name(name):
            return {
                'message': ITEM_ALREADY_EXISTS.format(name),
            }, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {
                'message': INSERTION_ERROR,
            }, 500

        return item.json(), 201

    @classmethod
    def put(cls, name: str) -> Tuple:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json(), 200

    @classmethod
    @jwt_required
    def delete(cls, name: str) -> Tuple:
        claims = get_jwt_claims()  # we added a claim 'is_admin' in app.py
        if claims['is_admin']:
            item = ItemModel.find_by_name(name)

            if item:
                item.delete_from_db()
                return {'message': ITEM_DELETED}, 200

            return {'message': ITEM_NOT_FOUND}, 404

        return {'message': ADMIN_REQUIRED}, 401


class ItemList(Resource):

    @classmethod
    @jwt_optional  # user logged in or non logged in can access different data
    def get(self) -> Tuple:
        user_id = get_jwt_identity()  # return None if non logged in
        items = [item.json() for item in ItemModel.find_all()]

        if user_id:
            return {'items': items}, 200

        return {
            'items': [item['name'] for item in items],
            'message': MORE_DATA,
        }, 200
