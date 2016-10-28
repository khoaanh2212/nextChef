from django.core.cache import get_cache
from django.shortcuts import redirect, render

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api_utils.views import CookboothWebAPIView
from backend.cache_utils import CacheUtils
from books.models import Book
from chefs.models import Chefs, Restaurant
from recipe.models import Recipes, Photos
from recipe.serializers import WebRecipeSerializer
from domain.book.Collaborators import Collaborators

from .serializers import LibraryChefSerializer

from infrastructure.recipe.RecipeRepository import RecipeRepository


class ChefRecipesListView(generics.ListAPIView):
    model = Recipes
    serializer_class = WebRecipeSerializer
    paginate_by = 12
    max_paginate_by = 12

    def get_queryset(self):
        if self.kwargs['chef_id'] == 'CHEF_ID':
            raise ParseError()

        chef_id = int(self.kwargs['chef_id'])

        if self.request.user.is_authenticated() and self.request.user.id == chef_id:
            return Recipes.objects.get_recipes_by_chef(chef_id, private=1)
        else:
            return Recipes.objects.get_recipes_by_chef(chef_id)


class ChefRecipesByNameListView(generics.ListAPIView):
    model = Recipes
    serializer_class = WebRecipeSerializer
    paginate_by = 5
    max_paginate_by = 5

    def get_queryset(self):
        recipe_repository = RecipeRepository.new()

        if self.kwargs['chef_id'] == 'CHEF_ID':
            raise ParseError()

        chef_id = int(self.kwargs['chef_id'])
        name = self.kwargs['name']

        public_recipe = recipe_repository.get_all_public(name)
        other_recipe = filter(lambda recipe: recipe.chef_id != chef_id, public_recipe)

        if self.request.user.is_authenticated() and self.request.user.id == chef_id:
            return Recipes.objects.get_recipes_by_chef_and_name(chef_id, name, private=1) + other_recipe
        else:
            return Recipes.objects.get_recipes_by_chef_and_name(chef_id, name) + other_recipe


class BookRecipesListView(generics.ListAPIView):
    model = Recipes
    serializer_class = WebRecipeSerializer
    paginate_by = 12
    max_paginate_by = 12

    def get_queryset(self):
        if self.kwargs['book_id'] == 'BOOK_ID':
            raise ParseError()

        book_id = int(self.kwargs['book_id'])
        chef_id = Book.objects.filter(pk=book_id).values_list('chef', flat=True)
        other_chef_ids = Book.objects.filter(pk=book_id)[0].chefs.all().values_list('id', flat=True)
        collaboratorInstance = Collaborators.new()
        listCollaborator = collaboratorInstance.collaboratorToList(Book.objects.filter(pk=book_id)[0].collaborators)
        if self.request.user.is_authenticated() and (
                self.request.user.id == chef_id[0] or self.request.user.id in other_chef_ids or self.request.user.id in listCollaborator):
            return Recipes.objects.get_recipes_by_book(book_id, private=1)
        else:
            return Recipes.objects.get_recipes_by_book(book_id)

class UploadRestaurantImageView(CookboothWebAPIView):
    def post(self, request, chef_id):
        try:
            chef = Chefs.objects.get(id=chef_id)

            if chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            restaurant, created = Restaurant.objects.get_or_create(chef=chef)
            restaurant.image = request.FILES['image']
            restaurant.save()

            cache = get_cache('default')
            restaurant_image_key = CacheUtils.get_key(CacheUtils.CHEF_RESTAURANT_IMAGE, chef_id=chef_id)
            restaurant_image = thumbnail_url(restaurant.image, 'library_restaurant_cover')
            cache.set(restaurant_image_key, restaurant_image)

            return Response({'success': True, 'url': restaurant.thumb_account_button})

        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class UploadAvatarImageView(CookboothWebAPIView):
    def post(self, request, chef_id):
        try:
            chef = Chefs.objects.get(id=chef_id)

            if chef != request.user:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

            photo, created = Photos.objects.get_or_create(chef=chef)

            photo.image_url = request.FILES['image']
            photo.save()

            photo.s3_url = photo.image_url.url  # Ensure same value as image_url
            photo.save()

            cache = get_cache('default')
            chef_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_AVATAR, chef_id=chef_id)
            chef_avatar = thumbnail_url(chef.avatar, 'chef_avatar')
            cache.set(chef_avatar_key, chef_avatar)

            chef_base_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_BASE_NAV_AVATAR, chef_id=chef_id)
            chef_base_avatar = thumbnail_url(chef.avatar, 'base_nav_avatar')
            cache.set(chef_base_avatar_key, chef_base_avatar)

            if chef == request.user:
                avatar_key = CacheUtils.get_key(CacheUtils.USER_AVATAR, user_id=chef_id)
                avatar = thumbnail_url(photo.image_url, 'base_nav_avatar')
                cache.set(avatar_key, avatar)

            return Response({'success': True, 'url': chef.avatar_thumb('chef_avatar')})

        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class UploadCoverImageView(CookboothWebAPIView):
    def post(self, request, chef_id):
        try:
            chef = Chefs.objects.get(id=chef_id)

            if chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            chef.cover = request.FILES['image']
            chef.save()

            cache = get_cache('default')
            chef_cover_key = CacheUtils.get_key(CacheUtils.CHEF_COVER, chef_id=chef_id)
            chef_cover = thumbnail_url(chef.cover, 'library_cover')
            cache.set(chef_cover_key, chef_cover)

            chef_edit_cover_key = CacheUtils.get_key(CacheUtils.CHEF_EDIT_COVER, chef_id=chef_id)
            chef_edit_cover = thumbnail_url(chef.cover, 'library_edit_modal_cover')
            cache.set(chef_edit_cover_key, chef_edit_cover)

            chef_key = CacheUtils.get_key(CacheUtils.CHEF, chef_id=chef_id)
            cache.set(chef_key, chef)

            return Response({'success': True, 'url': chef.cover_thumb('library_edit_modal_cover')})

        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class ListFollowersView(CookboothWebAPIView):
    def get(self, request, chef_id):
        try:
            chef_id = int(chef_id)
        except ValueError:
            return render(request, '410.html', status=410)

        cache = get_cache('default')
        list_followers_key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_LIST_10, chef_id=chef_id)
        list_followers = cache.get(list_followers_key, None)
        if list_followers is None:
            chef = get_object_or_404(Chefs, pk=chef_id)
            queryset = chef.followers.all()[:10]
            serializer = LibraryChefSerializer(queryset, many=True)
            list_followers = serializer.data
            cache.set(list_followers_key, list_followers)

        return Response({'success': True, 'followers': list_followers})


class ListFollowingView(CookboothWebAPIView):
    def get(self, request, chef_id):
        try:
            chef_id = int(chef_id)
        except ValueError:
            return render(request, '410.html', status=410)

        cache = get_cache('default')
        list_followings_key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_LIST_10, chef_id=chef_id)
        list_followings = cache.get(list_followings_key, None)
        if list_followings is None:
            chef = get_object_or_404(Chefs, pk=chef_id)
            queryset = chef.following.all()[:10]
            serializer = LibraryChefSerializer(queryset, many=True)
            list_followings = serializer.data
            cache.set(list_followings_key, list_followings)

        return Response({'success': True, 'following': list_followings})
