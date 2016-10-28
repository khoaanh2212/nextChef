from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.views import CookboothAPIView
from chefs.models import Chefs
from chefs.serializers import APIV1ChefsSerializer

from ..models import Recipes, Shares
from ..serializers import ApiShareSerializer


class ShareView(ListModelMixin, CookboothAPIView):
    serializer_class = APIV1ChefsSerializer

    def post(self, request, *args, **kwargs):
        """
        Share a recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        serializer = ApiShareSerializer(data=request.DATA, files=request.FILES)
        serializer.user = request.user
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            recipe.update_shares()
            return Response({'share': serializer.data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        Get 'shares' of a recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private:
            return self.invalid_request('The recipe is private')
        self.queryset = Chefs.objects.filter(shares__recipe=recipe)
        return self.list(request, *args, **kwargs)
