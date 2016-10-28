from legacy_wrapper.book_wrapper import Book
from infrastructure.BaseRepository import BaseRepository
from itertools import chain
from django.db.models import Q


class BookRepository(BaseRepository):
    @staticmethod
    def new():
        return BookRepository(model=Book)

    def getBooksByCollaborator(self, chef, collaborator_id):
        keyword = '[%d]' % collaborator_id
        return self.model.objects.filter(chef=chef) \
            .filter(collaborators__contains=keyword)

    def get_recipe_by_books(self, books):
        recipes = list()
        for book in books:
            recipes.extend(list(book.recipes.filter(draft=False)))
        return recipes

    def is_recipe_belong_to_public_book(self, recipe):
        books = list(self.model.objects.filter(recipes=recipe))
        for book in books:
            if not book.book_type is 'P' and not book.private:
                return True
        return False

    def get_book_by_chef(self, chef):
        keyword = '[%d]' % chef.id
        return self.model.objects.filter(Q(chef=chef) | Q(collaborators__contains=keyword)).order_by('name')

    def get_recipe_by_chef(self, chef):
        keyword = '[%d]' % chef.id
        books = self.model.objects.filter(
            (Q(chef=chef) | Q(collaborators__contains=keyword)) |
            (Q(book_type='N') & Q(private=False) & Q(status='A'))
        )
        return list(set(self.get_recipe_by_books(books)))

    def get_recipe_in_public_books(self):
        books = self.model.objects.filter(Q(book_type='N') & Q(private=False) & Q(status='A'))
        return list(set(self.get_recipe_by_books(books)))

    def get_recipe_by_following_chef(self, chef):
        books = self.model.objects.filter(Q(chef__in=chef.following.all()) & Q(book_type='N')
                                          & Q(private=False) & Q(status='A'))
        return list(set(self.get_recipe_by_books(books)))

    def is_collaborator_of_recipe(self, chef_id, recipe):
        if not chef_id:
            return False
        keyword = '[%d]' % chef_id
        books = list(self.model.objects.filter(recipes=recipe).filter(collaborators__icontains=keyword))
        return len(books) > 0
