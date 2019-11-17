# Mashmallow allow to convert a class to a Schema
# to transform object as dictionary (serialization):
from marshmallow import Schema, fields


class BookSchema(Schema):  # defines what a 'book' data is for users

    title = fields.Str()  # value associated to 'title' will be a string
    author = fields.Str()


class Book:  # defines what a 'book' is for the program

    def __init__(self, title, author, description):
        self.title = title
        self.author = author
        self.description = description  # will not be t serialized


book = Book(
    "Clean Code", "Robert Martin", "A book about writing cleaner code."
)

print("=" * 30)
print("With Book.__str__() method:")
print(book)

# Serializing the object to obtain a dictionary:
book_schema = BookSchema()
serialized_book = book_schema.dump(book)

print("=" * 30)
print("With BookSchema:")
print(serialized_book)
