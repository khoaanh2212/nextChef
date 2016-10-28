from random import shuffle

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny

from api_utils.views import CookboothAPIView, request_from_app
from books.models import Book
from chefs.models import Chefs
from colls.models import Collection

from .models import Recipes
from .serializers_v1 import (APIV1RecipesSerializer, ApiV1ExploreRecipeSerializer,
                             ApiV1RecommendPaginatedSerializer)


class RecipesListView(ListModelMixin, CookboothAPIView):
    serializer_class = APIV1RecipesSerializer

    def dispatch(self, request, *args, **kwargs):
        # Deactivate authentication for legacy URL
        if request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super(RecipesListView, self).dispatch(request, *args, **kwargs)

    def get_paginate_by(self):
        if request_from_app(self.request):
            return 10
        return 27

    def get(self, request, *args, **kwargs):
        key = kwargs.get('type', 'error')
        logged = request.user.is_authenticated()

        if logged:
            APIV1RecipesSerializer.user = request.user
        else:
            APIV1RecipesSerializer.user = None
        if key == 'all':
            if logged:
                self.queryset = Recipes.objects.explore_recipes(chef=request.user)
            else:
                self.queryset = Recipes.objects.explore_recipes()

        elif key == 'pro':
            if logged:
                self.queryset = Recipes.objects.explore_recipes_pros(chef=request.user)
            else:
                self.queryset = Recipes.objects.explore_recipes_pros()

        elif key == 'foodie':
            if logged:
                self.queryset = Recipes.objects.explore_recipes_foodies(chef=request.user)
            else:
                self.queryset = Recipes.objects.explore_recipes_foodies()

        elif key == 'followings':
            if logged:
                self.queryset = Recipes.objects.search_explore(chef=request.user)
            else:
                raise PermissionDenied()
        else:
            raise Http404()

        return self.list(request, *args, **kwargs)


class RecipeRecommendedView(ListModelMixin, CookboothAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ApiV1ExploreRecipeSerializer
    pagination_serializer_class = ApiV1RecommendPaginatedSerializer

    ITEMS_PER_PAGE = {
        'default': {'recipes': 6, 'books': 2, 'colls': 1, 'noted': 3, 'chefs': 1},
        'web': {'recipes': 14, 'books': 1, 'colls': 2, 'noted': 10, 'chefs': 3},
    }

    def get_paginate_by(self, queryset=None):
        key = 'web' if self.request.GET.get('web') == '1' else 'default'
        return self.ITEMS_PER_PAGE[key]['recipes']

    def _cache(self, key, query):
        cannon_key = 'recommended:%s:CANNON' % key
        if cannon_key not in cache:
            cache.set(cannon_key, [i['pk'] for i in query.values('pk')], 60 * 10)  # 10 minutes

        user_key = 'recommended:%s:%s' % (key, self.user.pk or 0)
        if user_key not in cache:
            ids_list = cache.get(cannon_key)
            shuffle(ids_list)
            cache.set(user_key, ids_list, 60 * 30)  # 30 minuts
            return ids_list
        else:
            return cache.get(user_key)

    def get(self, request, *args, **kwargs):
        """
        Recommend view
        """
        # Recipes
        self.queryset = Recipes.objects.explore_recipes(request.user).filter(noted=False)
        # Books
        self.books_queryset = Book.objects.recommended(request.user)
        # Chefs
        self.chefs_queryset = Chefs.objects.recommended(request.user)

        self.user = request.user
        # Collections
        self.colls_pks = self._cache('COLLS', Collection.objects.all())
        self.colls_queryset = Collection.objects.all()
        # Noted recipes
        self.noted_pks = self._cache('NOTED', Recipes.objects.filter(noted=True))
        self.noted_queryset = Recipes.objects.all()
        return self.list(request, *args, **kwargs)

    def get_serializer_context(self):
        ret = super(RecipeRecommendedView, self).get_serializer_context()
        ret['books'] = self.books_queryset
        ret['chefs'] = self.chefs_queryset
        ret['colls'] = self.colls_queryset
        ret['colls_pks'] = self.colls_pks
        ret['noted'] = self.noted_queryset
        ret['noted_pks'] = self.noted_pks

        key = 'web' if self.request.GET.get('web') == '1' else 'default'
        ret['items_per_page'] = self.ITEMS_PER_PAGE[key]
        return ret
