from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from api_utils.views import CookboothAPIView

from ..models import Recipes, Tags, RecipesHasTags
from ..serializers import ApiTagSerializer


class TagView(CookboothAPIView):
    def post(self, request, *args, **kwargs):
        """
        Add tags to recipe
        """
        if 'pk' in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        serializer = ApiTagSerializer(data=request.DATA, files=request.FILES)
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            return Response({'tag': serializer.data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        Get the tags of a recipe
        """
        if 'pk' in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        tags = [{'id': i.pk, 'name': i.name} for i in recipe.tags.all()]
        return Response({'tags': tags})

    def delete(self, request, *args, **kwargs):
        """
        Delete tag of recipe
        """
        if 'pk' not in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        tag = Tags.objects.get(pk=kwargs['pk'])

        if recipe.tags.filter(pk=tag.pk).exists():
            obj = RecipesHasTags.objects.get(recipe=recipe, tag=tag)
            obj.delete()
        else:
            return self.invalid_request('Tag not in recipe')
        return Response({'response': {'return': True}})
