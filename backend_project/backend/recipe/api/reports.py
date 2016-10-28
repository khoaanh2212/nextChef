from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from api_utils.views import CookboothAPIView

from ..models import Recipes, Report
from ..serializers import ApiReportSerializer


class ReportView(CookboothAPIView):
    def post(self, request, *args, **kwargs):
        """
        Report a recipe
        """
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        serializer = ApiReportSerializer(data=request.DATA, files=request.FILES)
        serializer.user = request.user
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            request.user.report_recipe(recipe)
            return Response({'report': serializer.data})
        return self.invalid_serializer_response(serializer)
