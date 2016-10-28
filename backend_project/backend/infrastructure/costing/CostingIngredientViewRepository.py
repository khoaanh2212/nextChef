from django.conf import settings
from django.db.models import Q

from domain.costing.CostingIngredientView import CostingIngredientView
from infrastructure.BaseRepository import BaseRepository


class CostingIngredientViewRepository(BaseRepository):

    @staticmethod
    def new():
        return CostingIngredientViewRepository(model=CostingIngredientView)

    def _make_query(self, chef_id, filter):
        return self.model.objects.filter(Q(chef_id=chef_id) | Q(chef_id__isnull=True))\
            .filter(ingredient__icontains=filter)\
            .exclude(Q(deleted__icontains=chef_id), Q(deleted__isnull=False))

    def find_by_chef_id(self, chef_id, filter = '', page = 1, is_suggestion_list = False, limit = settings.COSTING_PAGE_LIMIT):

        if is_suggestion_list:
            limit = settings.INGREDIENT_SUGGESTION_LIMIT

        page = page - 1
        start = page * limit
        end = (page + 1) * limit

        return self._make_query(chef_id, filter).order_by('ingredient')[start:end]

    def count_by_chef_id(self, chef_id, filter = ''):
        return self._make_query(chef_id, filter).count()
