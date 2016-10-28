from __future__ import absolute_import

from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin

from api_utils.views import CookboothAPIView

from books.serializers import ApiBookSerializer, ApiBookPaginatedSerializer

from ..models import Recipes


class BookView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiBookSerializer
    pagination_serializer_class = ApiBookPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the user books a recipe belongs to
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        if recipe.draft:
            return self.invalid_request('The recipe is a draft')

        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        self.queryset = recipe.book_set.filter(chef=request.user)
        ApiBookSerializer.user = request.user
        return self.list(request, *args, **kwargs)
