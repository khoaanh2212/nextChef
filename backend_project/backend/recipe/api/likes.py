from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.views import CookboothAPIView
from chefs.models import Chefs
from chefs.serializers import APIV1ChefsSerializer
from notifications.models import Notification

from ..models import Recipes, Likes


class LikeView(ListModelMixin, CookboothAPIView):
    serializer_class = APIV1ChefsSerializer

    def post(self, request, *args, **kwargs):
        """
        Like recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        try:
            like = Likes.objects.get(recipe=recipe, chef=request.user)
            return self.invalid_request('Like already exists')
        except Likes.DoesNotExist:
            like = Likes.objects.create(recipe=recipe, chef=request.user)
            recipe.update_likes()
            if request.user != recipe.chef:     # Don't send notification when user do a self like
                Notification.create_new_like(like)
            return Response({'response': {'return': True}})

    def delete(self, request, *args, **kwargs):
        """
        Unlike recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        try:
            like = Likes.objects.get(recipe=recipe, chef=request.user)
            like.delete()
            recipe.update_likes()
            return Response({'response': {'return': True}})
        except Likes.DoesNotExist:
            raise Http404()

    def get(self, request, *args, **kwargs):
        """
        Get 'likes' of a recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private:
            return self.invalid_request('The recipe is private')
        self.queryset = Chefs.objects.filter(likes__recipe=recipe)
        return self.list(request, *args, **kwargs)
