from django.conf import settings
from django.db.models import Q
from infrastructure.BaseRepository import BaseRepository
from domain.recipe.RecipeSuggestionView import RecipeSuggestionView
from books.models import Book
from recipe.models import Recipes


class RecipeSuggestionViewRepository(BaseRepository):
    @staticmethod
    def new():
        return RecipeSuggestionViewRepository(model=RecipeSuggestionView)

    def _make_query(self, chef, filter):

        collaborator_keyword = '[%d]' % chef.id
        c_k1 = ',%d' % chef.id
        c_k2 = '%d,' % chef.id
        c_k3 = ',%d,' % chef.id

        return self.model.objects.filter(
            Q(chef_id=chef.id) | Q(chef_id__in=c_k1) | Q(chef_id__in=c_k2) | Q(chef_id__in=c_k3) |
            Q(collaborators__contains=collaborator_keyword) |
            (~Q(book_type=Book.PRIVATE) & ~Q(recipe_is_draft=True))) \
                      .exclude(~Q(recipe_name__icontains=filter))

    def find_by_chef(self, chef, filter='', page=1, limit=settings.RECIPE_SUGGESTION_LIMIT):

        page = page - 1
        start = page * limit
        end = (page + 1) * limit

        recipes = self._make_query(chef, filter).distinct()[start:end]

        return list(recipes)

    def count_by_chef(self, chef, filter=''):

        return self._make_query(chef, filter).count()

