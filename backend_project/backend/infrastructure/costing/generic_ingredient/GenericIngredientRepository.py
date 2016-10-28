from django.conf import settings
from django.db.models import Q

from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from infrastructure.BaseRepository import BaseRepository


class GenericIngredientRepository(BaseRepository):

    @staticmethod
    def new():
        return GenericIngredientRepository(model=GenericIngredient)

    def findAll(self, filter = '', page = 1, limit = settings.COSTING_PAGE_LIMIT):
        page = page - 1
        start = page * limit
        end = (page + 1) * limit
        return self.model.objects\
            .filter(Q(ingredient__icontains=filter))\
            .order_by('ingredient')[start:end]
