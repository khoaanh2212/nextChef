import json
from django.core.cache import get_cache

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from api_utils.views import CookboothAPIView
from backend.cache_utils import CacheUtils
from notifications.models import Notification
from recipe.models import Recipes, ChefsHasRecipes
from recipe.serializers import (ApiPhotoSerializer, ApiPhotoPaginatedSerializer,
                                ApiRecipeSerializer, ApiRecipePaginatedSerializer,
                                ApiRecipePreviewSerializer, ApiPhotoPreviewSerializer)

from .models import Book, ChefsHasBooks, BookHasRecipes
from .serializers import ApiBookSerializer, WebBookSerializer
from application.book.BookApplicationService import BookApplicationService
import traceback


class AddBookView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        try:
            book_name = request.POST.get('name')
            book_private = request.POST.get('private') == "1"
            book_collaborators = request.POST.get('collaborators', "")
            book_type = 'P' if book_private else 'N'

            if book_name == '':
                return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

            book = Book.objects.create(
                name=book_name,
                private=book_private,
                chef=request.user,
                book_type=book_type
            )

            book_application_service = BookApplicationService.new()
            book_application_service.set_book_collaborators(book, book_collaborators, request)

            book_serializer = WebBookSerializer(book)

            cache = get_cache('default')
            key = CacheUtils.get_key(CacheUtils.CHEF_BOOKS, chef_id=request.user.id)
            cache.set(key, None)

            return Response({'success': True, 'book': book_serializer.data}, status=status.HTTP_200_OK)

        except Exception, e:
            print Exception, e
            traceback.print_exc()
            return Response({'success': False, 'message': 'Can not adding book'}, status=status.HTTP_400_BAD_REQUEST)


class AddRecipeToBookView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, book_id, recipe_id):
        try:
            from django.db.models import get_model

            model_class = get_model('books', 'Book')
            book = model_class.objects.get(pk=book_id)

            if request.user != book.chef:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            recipe = Recipes.objects.get(id=recipe_id)

            if recipe.chef != book.chef and \
                    not ChefsHasRecipes.objects.filter(chef=book.chef, recipe=recipe).exists():
                ChefsHasRecipes.objects.create(chef=book.chef, recipe=recipe)
                Notification.create_new_copy_recipe(recipe, book.chef)

            if not book.has_recipe(recipe):
                book.add_recipe(recipe)
                # Events.track(request.user.email, Events.EVENT_RECIPE_TO_BOOK)
                cache = get_cache('default')
                key = CacheUtils.get_key(CacheUtils.CHEF_BOOKS, chef_id=request.user.id)
                cache.set(key, None)
                return Response({'success': True, 'added': True}, status=status.HTTP_200_OK)
            else:
                book.delete_recipe(recipe)
                cache = get_cache('default')
                key = CacheUtils.get_key(CacheUtils.CHEF_BOOKS, chef_id=request.user.id)
                cache.set(key, None)
                return Response({'success': True, 'added': False}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class EditBookView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)

            if book.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            new_name = str(request.POST.get('name', ''))
            new_private = int(request.POST.get('private', 0))
            new_collaborators = str(request.POST.get('collaborators', ''))
            book_application_service = BookApplicationService.new()
            new_collaborator_ids = book_application_service.decorate_collaborators(new_collaborators)
            book_application_service.send_email_collaborator_when_edit(book.collaborators, new_collaborator_ids, book,
                                                                       request)
            book.name = new_name
            book.private = new_private
            book.collaborators = new_collaborators
            book.save()
            cache = get_cache('default')
            key = CacheUtils.get_key(CacheUtils.CHEF_BOOKS, chef_id=request.user.id)
            cache.set(key, None)

            return Response({'success': True}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class DeleteBookView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            if book.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)
            book.delete()

            cache = get_cache('default')
            key = CacheUtils.get_key(CacheUtils.CHEF_BOOKS, chef_id=request.user.id)
            cache.set(key, None)

            return Response({'success': True}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class BookView(CookboothAPIView):
    http_method_names = CookboothAPIView.http_method_names + ['copy']

    def post(self, request, *args, **kwargs):
        """
        Create book
        """
        if 'pk' in kwargs:
            raise Http404()

        serializer = ApiBookSerializer(data=request.DATA)
        serializer.user = request.user
        if serializer.is_valid():
            book = serializer.save()
            return Response({'book': serializer.data})
        return self.invalid_serializer_response(serializer)

    def put(self, request, *args, **kwargs):
        """
        Update book
        """
        if 'pk' not in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['pk'])
        if book.chef != request.user:
            self.raise_invalid_credentials()

        serializer = ApiBookSerializer(book, data=request.DATA, partial=True)
        serializer.user = request.user
        if serializer.is_valid():
            book = serializer.save()
            return Response({'book': serializer.data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        View book
        """
        if 'pk' not in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['pk'])

        serializer = ApiBookSerializer(book, context={'most_popular_recipe_cover_image': True})
        serializer.user = request.user
        data = serializer.data

        if book.chef != request.user and not book.is_public:
            chef_added_book_ids = request.user.books_added.all().values_list('id', flat=True)
            if not book.id in chef_added_book_ids:
                return self.invalid_request('This book is not available')
        # if book.chef != request.user and not book.is_public:
        #    return self.invalid_request('This book is not public')

        data['nb_recipes'] = book.recipes_total
        data['nb_likes'] = book.likes_total

        return Response({'book': data})

    def delete(self, request, *args, **kwargs):
        """
        Delete book
        """
        if 'pk' not in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['pk'])

        if book.chef != request.user:
            self.raise_invalid_credentials()

        if book.can_be_sold:
            return self.invalid_request('A book for sale cannot be deleted')

        book.delete()
        return Response({'response': {'return': True}})

    def copy(self, request, *args, **kwargs):
        """
        Copy book
        """
        if 'pk' not in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['pk'])

        # The old API did allow to copy a book the user owned. We do not allow it
        if book.chef == request.user:
            return self.invalid_request('The chef is already the owner of this book')

        if not book.is_public:
            return self.invalid_request('This book is not public')

        if book.can_be_sold:
            return self.invalid_request('A book for sale cannot be copied')

        if not ChefsHasBooks.objects.filter(chef=request.user, book=book).exists():
            ChefsHasBooks.objects.create(chef=request.user, book=book)

        serializer = ApiBookSerializer(book)
        serializer.user = request.user

        data = serializer.data
        # For some reason the old API did not return these fields in this endpoint
        for f in 'nb_shares', 'nb_comments', 'nb_added':
            data.pop(f, None)
        return Response({'book': serializer.data})


class CollaboratorView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['pk'])
        collaborator_ids = book.collaborators

        book_application_service = BookApplicationService.new()
        data = book_application_service.getCollaborators(collaborator_ids)

        return Response({'collaborators': json.dumps(data)})


class RecipeView(ListModelMixin, CookboothAPIView):
    pagination_serializer_class = ApiRecipePaginatedSerializer

    def post(self, request, *args, **kwargs):
        """
        Add recipe to book
        """
        if 'pk' in kwargs:
            raise Http404()

        chef = request.user

        book = get_object_or_404(Book, pk=kwargs['book_pk'])
        if book.chef != chef:
            self.raise_invalid_credentials()

        recipe_id = request.REQUEST.get('recipe')
        try:
            recipe = Recipes.objects.get(pk=recipe_id)
        except Recipes.DoesNotExist:
            return self.invalid_request('Recipe not exists')

        if recipe.chef != chef and (recipe.private or recipe.draft):
            return self.invalid_request('Invalid recipe')

        if recipe.is_in_book_for_sale:
            return self.invalid_request('A recipe in a book for sale cannot be in other books')

        if book.book_type == Book.TO_SELL and recipe.chef != chef:
            return self.invalid_request('A book for sale cannot has recipes from other chefs')

        if BookHasRecipes.objects.filter(book=book, recipe=recipe).exists():
            return self.invalid_request('Recipe already in book')
        BookHasRecipes.objects.create(book=book, recipe=recipe)

        if recipe.chef != chef and \
                not ChefsHasRecipes.objects.filter(chef=chef, recipe=recipe).exists():
            ChefsHasRecipes.objects.create(chef=chef, recipe=recipe)
            Notification.create_new_copy_recipe(recipe, chef)

        # TODO: Update ChefsHasRecipes table accordingly

        return Response({'response': {'return': True}})

    def delete(self, request, *args, **kwargs):
        """
        Delete recipe from book
        """
        if 'pk' not in kwargs:
            raise Http404()

        chef = request.user

        book = get_object_or_404(Book, pk=kwargs['book_pk'])
        if book.chef != chef:
            self.raise_invalid_credentials()

        if book.can_be_sold:
            return self.invalid_request('A recipe cannot be deleted from a book for sale')

        recipe = Recipes.objects.get(pk=kwargs['pk'])

        if not BookHasRecipes.objects.filter(book=book, recipe=recipe).exists():
            return self.invalid_request('Recipe not in book')

        obj = BookHasRecipes.objects.get(book=book, recipe=recipe)
        obj.delete()

        if recipe.chef != chef:
            all_books = Book.objects.all_books(chef, show_private=True)
            if not BookHasRecipes.objects.filter(book__in=all_books, recipe=recipe).exists():
                obj = ChefsHasRecipes(chef=chef, recipe=recipe)
                obj.delete()

        return Response({'response': {'return': True}})

    def get_serializer_class(self):
        book = self.book
        user = self.request.user
        if not book.can_be_sold:
            return ApiRecipeSerializer
        return ApiRecipeSerializer if book.user_has_bought_it(user) else ApiRecipePreviewSerializer

    def get_serializer_context(self):
        ret = super(RecipeView, self).get_serializer_context()
        ret['user'] = self.request.user
        ret['return_user_properties'] = ('added', 'liked', 'shared', 'reported', 'commented')
        return ret

    def get(self, request, *args, **kwargs):
        """
        Show recipes of book
        """
        if 'pk' in kwargs:
            raise Http404()

        book = get_object_or_404(Book, pk=kwargs['book_pk'])
        show_private = book.chef == request.user

        if not show_private:
            chef_added_book_ids = request.user.books_added.all().values_list('id', flat=True)
            if book.id in chef_added_book_ids:
                show_private = True

        self.queryset = book.public_recipes(request.user, show_private)
        self.book = book

        return self.list(request, *args, **kwargs)


class PhotoView(ListModelMixin, CookboothAPIView):
    pagination_serializer_class = ApiPhotoPaginatedSerializer

    def get_serializer_class(self):
        book = self.book
        user = self.request.user
        if not book.can_be_sold:
            return ApiPhotoSerializer
        return ApiPhotoSerializer if book.user_has_bought_it(user) else ApiPhotoPreviewSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the photos of a book
        """
        book = get_object_or_404(Book, pk=kwargs['book_pk'])
        self.queryset = book.photos(request.user, False)
        self.book = book
        return self.list(request, *args, **kwargs)
