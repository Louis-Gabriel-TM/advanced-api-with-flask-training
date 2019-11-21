from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.ModelSchema):

    class Meta:
        model = ItemModel

        load_only = ('store_id',)
        dump_only = ('id',)
        include_fk = True
