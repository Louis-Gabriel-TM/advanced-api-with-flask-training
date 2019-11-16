from typing import Dict, List, Union

from db import db


# ItemJSON is a custom type. It is a Dict where keys are str
# and the values can be int, float or str:
ItemJSON = Dict[str, Union[int, float, str]]


class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    dtore = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:  # using custom type
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    @classmethod
    # type hinting with the current class:
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
