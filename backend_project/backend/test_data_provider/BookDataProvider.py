from books.models import Book
import copy


class BookDataProvider:
    def __init__(self, book = Book()):
        self.book = copy.deepcopy(book)

    def build(self):
        return self.book

    def with_id(self, id):
        self.book.id = id
        return self

    def with_name(self, name):
        self.book.name = name
        return self

    def with_chef(self, chef):
        self.book.chef = chef
        return self

    def with_book_type(self, book_type):
        self.book.book_type = book_type
        return self

    def publish(self):
        self.book.book_type = 'N'
        self.book.private = False
        return self

    def with_collaborators(self, collaborators):
        self.book.collaborators = collaborators
        return self

    @staticmethod
    def get():
        return BookDataProvider()

    @staticmethod
    def get_default():
        data_provider = BookDataProvider()
        return data_provider.build()
