from django.core.cache import get_cache
from django.http import Http404

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_utils.views import CookboothAPIView
from backend.cache_utils import CacheUtils
from books.models import Book
from books.serializers import ApiBookSpecialSerializer, ApiBookPaginatedSerializer
from recipe.models import Recipes
from recipe.serializers import ApiRecipeSerializer

from .models import Chefs
from .serializers import APIV1ChefsSerializer, ApiV1ByTypePaginatedSerializer


class ChefLovesListView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        chef_id = request.user.id
        loves_json = []
        cache = get_cache('default')
        key = CacheUtils.get_key(CacheUtils.USER_LOVES, user_id=request.user.id)
        loves_json = cache.get(key, None)
        if loves_json is None:
            chef = get_object_or_404(Chefs, pk=chef_id)
            loves_json = chef.json_loves_list
            cache.set(key, loves_json)
        return Response({'success': True, 'loves': loves_json}, status=status.HTTP_200_OK)


class ChefFollowingsListView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        chef_id = request.user.id
        followings_json = []
        cache = get_cache('default')
        key = CacheUtils.get_key(CacheUtils.USER_FOLLOWINGS, user_id=chef_id)
        followings_json = cache.get(key, None)
        if followings_json is None:
            chef = get_object_or_404(Chefs, pk=chef_id)
            followings_json = chef.json_follows_list
            cache.set(key, followings_json)
        return Response({'success': True, 'followings': followings_json}, status=status.HTTP_200_OK)


class ChefsListView(ListModelMixin, CookboothAPIView):
    serializer_class = APIV1ChefsSerializer

    def dispatch(self, request, *args, **kwargs):
        # Deactivate authentication for legacy URL
        if request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(ChefsListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self):
        return 3

    def get(self, request, *args, **kwargs):
        key = kwargs.get('type', 'error')
        if key == 'all':
            self.queryset = Chefs.objects.chefs_all()

        elif key == 'pro':
            self.queryset = Chefs.objects.chefs_pros()

        elif key == 'foodie':
            self.queryset = Chefs.objects.chefs_foodies()

        else:
            raise Http404()

        return self.list(request, *args, **kwargs)


class ChefsOnboardView(ListModelMixin, CookboothAPIView):
    permission_classes = (AllowAny, )
    serializer_class = APIV1ChefsSerializer

    def get(self, request, *args, **kwargs):
        """
        Get on-board chefs
        """
        self.queryset = Chefs.objects.filter(onboard_score__gt=0).order_by('-onboard_score', 'pk')
        lang = request.GET.get('lang')
        if lang:
            if lang not in Chefs.ONBOARD_LANGUAGES_CHOICES:
                raise Http404()
            self.queryset = self.queryset.filter(onboard_languages__contains=lang)
        return self.list(request, *args, **kwargs)


class ChefsByTypeListView(ListModelMixin, CookboothAPIView):
    serializer_class = APIV1ChefsSerializer
    pagination_serializer_class = ApiV1ByTypePaginatedSerializer
    paginate_by = 10

    def get_serializer_context(self):
        ret = super(ChefsByTypeListView, self).get_serializer_context()
        ret['pros'] = self.queryset_pros
        ret['brands'] = self.queryset_brands
        return ret

    def get(self, request, *args, **kwargs):
        """
        Get chefs by type
        """
        self.queryset = Chefs.objects.chefs_all().filter(type=Chefs.TYPE_FOODIE)
        self.queryset_pros = Chefs.objects.chefs_all().filter(type=Chefs.TYPE_PRO)
        self.queryset_brands = Chefs.objects.chefs_all().filter(type=Chefs.TYPE_BRAND)
        return self.list(request, *args, **kwargs)


class ChefBooksView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiBookSpecialSerializer
    pagination_serializer_class = ApiBookPaginatedSerializer

    def get_serializer_context(self):
        ret = super(ChefBooksView, self).get_serializer_context()
        ret['most_popular_recipe_cover_image'] = True
        return ret

    def get(self, request, *args, **kwargs):
        """
        Get all the books of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        show_private = chef == request.user
        self.queryset = Book.objects.all_books(chef, show_private=show_private)
        ApiBookSpecialSerializer.user = request.user
        return self.list(request, *args, **kwargs)


class ChefRecipesView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiRecipeSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all the recipes of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        show_private = chef == request.user
        query = Recipes.objects.all_chef_recipes(chef, show_private=show_private)
        self.queryset = query.order_by('-creation_date')
        return self.list(request, *args, **kwargs)
