from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from api_utils.views import CookboothAPIView
from colls.models import Collection
from colls.serializers import CollsSerializer


class CollsListView(ListModelMixin, CookboothAPIView):
    serializer_class = CollsSerializer

    #No dispatch. Called by APP, always auth user
    def get_paginate_by(self):
        return 4

    def get(self, request, *args, **kwargs):
        self.queryset = Collection.objects.filter(is_active=True)
        return self.list(request, *args, **kwargs)
