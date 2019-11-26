from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):

    class Meta:
        # Flask-Marshmallow allows to create the Schema as an extension of the Model:
        model = UserModel

        load_only = ('password',)  # can only becomes an object (for the API)
        dump_only = ('id', 'activated')  # can only becomes a dictionnary (for the user)
