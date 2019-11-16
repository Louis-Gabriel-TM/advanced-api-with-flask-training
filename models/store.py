from typing import Dict, List, Union

from db import db
from models.item import ItemJSON

# StoreJSON is another custom type. It is a Dict where keys are str
# and the values can be int, str or a list of ItemJSON, a previous
# custom type:
StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]


class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship('ItemModel', lazy='dynamic')
    # 'dynamic' indicates the items of a store can be query,
    # whether they were created before or after the store.

    def __init__(self, name: str) -> None:
        self.name = name

    def json(self) -> StoreJSON:  # using custom type
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    @classmethod
    # type hinting with the current class:
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
