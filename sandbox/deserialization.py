from marshmallow import Schema, fields


class BookSchema(Schema):

    title = fields.Str(required=True)
    author = fields.Str(required=True)
    description = fields.Str()


class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author


incoming_book_data = {
    'title': "Clean Code",
    'author': "Robert Martin",
}

# BookSchema(unknown=INCLUDE/EXCLUDE) can handle unexpected data:
book_schema = BookSchema()
deserialized_book = book_schema.load(incoming_book_data)

print("=" * 30)
print("Deserialized data:")
print(deserialized_book)

book_object = Book(**deserialized_book)

print("=" * 30)
print("As a program object:")
print(book_object, book_object.title)
