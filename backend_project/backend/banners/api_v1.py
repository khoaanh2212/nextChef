from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from api_utils.views import CookboothAPIView
from banners.models import Banner
from banners.serializers import BannersSerializer


class BannersListView(ListModelMixin, CookboothAPIView):
    serializer_class = BannersSerializer

    def dispatch(self, request, *args, **kwargs):
        # Deactivate authentication for legacy URL
        if request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(BannersListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self):
        return 4

    def get(self, request, *args, **kwargs):
        self.queryset = Banner.objects.filter(is_active=True).order_by('-score')
        return self.list(request, *args, **kwargs)
