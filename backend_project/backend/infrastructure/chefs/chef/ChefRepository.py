from infrastructure.BaseRepository import BaseRepository
from chefs.models import Chefs
from django.db.models import Q


class ChefRepository(BaseRepository):
    def __init__(self, model=Chefs):
        BaseRepository.__init__(self, model)

    @staticmethod
    def new(model=Chefs):
        return ChefRepository(model)

    def get_chef_by_name(self, name, limit=1):
        start = (20 * limit) - 20
        end = 20 * limit + 1
        return self.model.objects \
                   .filter(Q(name__icontains=name) | Q(surname__icontains=name) | Q(email__icontains=name)) \
                   .order_by('name')[start:end]

    def get_chef_by_list_id(self,arrId):
        return self.model.objects.filter(Q(pk__in=arrId))

    def get_chef_by_email(self, email):
        return self.model.objects.filter(email=email)
