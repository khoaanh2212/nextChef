from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.renderers import IgnoreClientContentNegotiation
from api_utils import str_to_datetime
from api_utils.views import CookboothAPIView

from ..models import Recipes, Photos, PhotoFilters, PhotoStyles
from ..serializers import ApiPhotoSerializer, ApiPhotoPaginatedSerializer, ApiPhotoStyleSerializer


class PhotoView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiPhotoSerializer
    pagination_serializer_class = ApiPhotoPaginatedSerializer

    def post(self, request, *args, **kwargs):
        """
        Add photo to recipe
        """
        if 'pk' in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        serializer = ApiPhotoSerializer(data=request.DATA, files=request.FILES)
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            for f in 'cover', 'order', 'instructions', 'time', 'temperature', 'quantity', 'recipe':
                data.pop(f, None)
            return Response({'photo': data})
        return self.invalid_serializer_response(serializer)

    def put(self, request, *args, **kwargs):
        """
        Update photo of recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        obj = get_object_or_404(Photos, pk=kwargs['pk'])

        serializer = ApiPhotoSerializer(obj, data=request.DATA, files=request.FILES, partial=True)
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            return Response({'photo': serializer.data})
        return self.invalid_serializer_response(serializer)

    def delete(self, request, *args, **kwargs):
        """
        Delete photo of recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        obj = Photos.objects.get(pk=kwargs['pk'])
        obj.delete()
        return Response({'response': {'return': True}})

    def get(self, request, *args, **kwargs):
        """
        Get the photos of a recipe
        """
        if 'pk' in kwargs:
            raise Http404()

        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.private and recipe.chef != request.user:
            return self.invalid_request('The recipe is private and the requestor is not the owner')

        queryset = recipe.photos.all()

        book = recipe.book_for_sale()
        if book and not book.user_has_bought_it(request.user):
            queryset = queryset[:1]

        self.queryset = queryset

        return self.list(request, *args, **kwargs)


class UpdatedPhotosView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiPhotoSerializer
    pagination_serializer_class = ApiPhotoPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the photos of a user sorted by recent changes
        """
        date = request.GET.get('date')
        if not date or not date.isdigit():
            return self.invalid_request('Missing date field')

        date = str_to_datetime(date)
        self.queryset = Photos.objects.latest_updated(request.user, date).select_related('recipe')
        return self.list(request, *args, **kwargs)


class StyleView(CookboothAPIView):
    content_negotiation_class = IgnoreClientContentNegotiation

    def dispatch(self, request, *args, **kwargs):
        # Deactivate authentication for legacy URL
        if kwargs['action'] == 'photos':
            self.authentication_classes = ()
            self.permission_classes = ()
        return super(StyleView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photos, pk=kwargs['pk'])
        photo_filter = get_object_or_404(PhotoFilters, name=kwargs['filter'])

        if kwargs['action'] != 'photos':
            if photo.recipe and photo.recipe.chef != request.user and photo.recipe.private:
                error = 'The recipe is private and the requestor is not the owner'
                return self.invalid_request(error)
        else:
            # Sanity check for photo rows without files
            if photo.s3_url.name is None and photo.image_url.name is None:
                raise Http404()

        try:
            styles = PhotoStyles.objects.filter(photo=photo, filter=photo_filter)[:1]
            style = styles[0]
        except (PhotoStyles.DoesNotExist, IndexError):
            try:
                style = PhotoStyles(photo=photo, filter=photo_filter)
                filtered_photo_file = photo_filter.apply_to_photo(photo)
                style.s3_url.save(photo.s3_url.name, filtered_photo_file)
                style.save()
            except (IOError, ValueError):
                raise Http404()

        if kwargs['action'] == 'photos':
            # Avoid Suspicious operation error with legacy file names.
            if style.s3_url:
                if 'http:' in style.s3_url.name:
                    url = style.s3_url.name
                else:
                    url = style.s3_url.url
            else:
                url = '/404'
            return redirect(url)

        serializer = ApiPhotoStyleSerializer(style)
        return Response({'style': serializer.data})
