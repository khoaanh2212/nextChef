from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.views import CookboothAPIView
from notifications.models import Notification

from ..models import Recipes, Comments
from ..serializers import ApiCommentSerializer, ApiCommentPaginatedSerializer


class CommentView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiCommentSerializer
    pagination_serializer_class = ApiCommentPaginatedSerializer

    def post(self, request, *args, **kwargs):
        """
        Add comment to recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        book = recipe.book_for_sale()
        if book and not book.user_has_bought_it(request.user):
            return self.invalid_request('Recipe in book for sale and the user has not bought it')

        serializer = ApiCommentSerializer(data=request.DATA, files=request.FILES)
        serializer.user = request.user
        serializer.recipe = recipe
        if serializer.is_valid():
            comment = serializer.save()
            recipe.update_comments()
            if request.user != recipe.chef:
                Notification.create_new_comment(comment)
            Notification.send_new_comment_to_thread(comment)
            return Response({'comment': serializer.data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        Get the comments of a recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        self.queryset = recipe.comments.select_related('chef').all()
        return self.list(request, *args, **kwargs)
