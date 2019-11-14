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


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    def get(self, name: str) -> Tuple:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {'message': "Item not found."}, 404

    @fresh_jwt_required
    def post(self, name: str) -> Tuple:
        if ItemModel.find_by_name(name):
            return {
                'message': f"An item with name '{name}' already exists.'"
            }, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {
                'message': "An error occured while inserting the item."
            }, 500

        return item.json(), 201

    def put(self, name: str) -> Tuple:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json(), 200

    @jwt_required
    def delete(self, name: str) -> Tuple:
        claims = get_jwt_claims()  # we added a claim 'is_admin' in app.py
        if claims['is_admin']:
            item = ItemModel.find_by_name(name)

            if item:
                iteme.delete_from_db()
                return {'message': "Item deleted."}, 200

            return {'message': "Item not found."}, 404
        
        return {'message': "Admin privileges required."}, 401


class ItemList(Resource):
    
    @jwt_optional  # user logged in or non logged in can access different data
    def get(self) -> Tuple:
        user_id = get_jwt_identity()  # return None if non logged in
        items = [item.json() for item in ItemModel.find_all()]

        if user_id:
            return {'items': items}, 200

        return {
            'items': [item['name'] for item in items],
            'message': "More data available if you log in."
        }, 200
