from ma import ma
from models.user import UserModel


class UserSchema(Schema):

    class Meta:
        # Flask-Marshmallow allows to create the Schema as an extension of the Model:
        model = UserModel

        load_only = ('password',)  # can only becomes an object (for the API)
        dump_only = ('id',)  # can only becomes a dictionnary (for the user)

"""     id = fields.Int()  # auto-incremented
    username = fields.Str(required=True)
    password = fields.Str(required=True) """
