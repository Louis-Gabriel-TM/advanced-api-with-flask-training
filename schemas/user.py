from marshmallow import Schema, fields


class UserSchema(Schema):

    class Meta:
        load_only = ('password',)  # can only becomes an object (for the API)
        dump_only = ('id',)  # can only becomes a dictionnary (for the user)

    id = fields.Int()  # auto-incremented
    username = fields.Str(required=True)
    password = fields.Str(required=True)
