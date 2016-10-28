from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils import str_to_datetime
from api_utils.views import CookboothAPIView
from notifications.models import Notification
from ..models import Recipes, ChefsHasRecipes

from ..searchers import RecipeMapping
from ..serializers import ApiRecipeSerializer, ApiRecipePaginatedSerializer
from ..serializers_v1 import ApiV1ExploreRecipeSerializer
from application.recipe.RecipeApplicationService import RecipeApplicationService


class RecipeView(CookboothAPIView):
    http_method_names = CookboothAPIView.http_method_names + ['copy']

    def remove_unwanted_data(self, data):
        """
        For some reason in create and update there are fields that didn't appear in the original
        API. Remove them after the serialzer has returned the data. Probably unnecessary
        """
        for f in 'nb_added', 'nb_likes', 'nb_shares', 'nb_comments':
            data.pop(f, None)
        return data

    def post(self, request, *args, **kwargs):
        """
        Create recipe
        """
        if 'pk' in kwargs:
            raise Http404()

        serializer = ApiRecipeSerializer(data=request.DATA, files=request.FILES)
        serializer.user = request.user
        if serializer.is_valid():
            recipe = serializer.save()
            data = self.remove_unwanted_data(serializer.data)
            return Response({'recipe': data})
        return self.invalid_serializer_response(serializer)

    def put(self, request, *args, **kwargs):
        """
        Update recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Recipes, pk=kwargs['pk'])
        if obj.chef != request.user:
            self.raise_invalid_credentials()

        # Check if we have a new publication
        if obj.draft and request.DATA['draft'] == '0' and request.DATA['private'] == '0':
            notify_new = True
        else:
            notify_new = False

        serializer = ApiRecipeSerializer(obj, data=request.DATA, files=request.FILES, partial=True)
        serializer.user = request.user
        if serializer.is_valid():
            recipe = serializer.save()
            if notify_new:
                Notification.create_new_recipe(recipe)
            data = self.remove_unwanted_data(serializer.data)
            return Response({'recipe': data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        View recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Recipes, pk=kwargs['pk'])

        draft = request.GET.get('draft', '')
        if draft in ('', '0') and obj.draft:
            return self.invalid_request('The recipe is a draft and there is no parameter draft')

        if obj.private and obj.chef != request.user:
            allowed = False
            chef_added_book_ids = request.user.books_added.all().values_list('id',flat=True)
            from books.models import BookHasRecipes
            
            from django.db.models import get_model
            bookHasRecipesModel = get_model('books', 'BookHasRecipes')
            
            recipe_book_ids = bookHasRecipesModel.objects.filter(recipe=obj).values_list('book',flat=True)
            for chef_added_book_id in chef_added_book_ids:
                if chef_added_book_id in recipe_book_ids:
                    allowed = True
                    break
            if not allowed:
                return self.invalid_request('The recipe is private and the requestor is not the owner')

        serializer = ApiRecipeSerializer(obj)
        serializer.return_user_properties = ('added', 'liked', 'shared', 'reported', 'commented')
        serializer.user = request.user
        data = serializer.data
        return Response({'recipe': data})

    def delete(self, request, *args, **kwargs):
        """
        Delete recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Recipes, pk=kwargs['pk'])
        if obj.chef != request.user:
            self.raise_invalid_credentials()
        obj.delete()
        return Response({'response': {'return': True}})

    def copy(self, request, *args, **kwargs):
        """
        Copy recipe
        """
        if 'pk' not in kwargs:
            raise Http404()

        recipe = get_object_or_404(Recipes, pk=kwargs['pk'])
        if recipe.chef == request.user:
            return self.invalid_request('The chef is already the owner of this recipe')
        if recipe.draft:
            return self.invalid_request('The recipe is a draft')
        if recipe.private:
            return self.invalid_request('The recipe is private')
        if recipe.is_in_book_for_sale:
            return self.invalid_request('A recipe in book for sale cannot be copied')

        if not ChefsHasRecipes.objects.filter(chef=request.user, recipe=recipe).exists():
            ChefsHasRecipes.objects.create(chef=request.user, recipe=recipe)
            recipe.update_adds()
            Notification.create_new_copy_recipe(recipe, request.user)

        if 'books' in request.GET:
            # In the original PHP code there was two odd things:
            # 1. The request returned a 400 error if one of the books ids did not exist. But
            #    it created the relation (recipe, chef) anyway and all the relations (recipe, book)
            #    previously processed until failing id
            #    - Here we will just ignore the non existing books
            # 2. It allowed to add the recipe to a book that was not owned by the user sending
            #    the request, the only requirement was the book existed
            #    - Here we do not allow that and will just ignore the book
            books_ids = request.GET['books']
            books = Books.objects.filter(chef=request.user, pk__in=books_ids)
            for book in books:
                book.add_recipe(recipe)

        serializer = ApiRecipeSerializer(recipe)
        serializer.user = request.user
        data = self.remove_unwanted_data(serializer.data)
        return Response({'recipe': data})


class RecipeSearchView(ListModelMixin, CookboothAPIView):
    pagination_serializer_class = ApiRecipePaginatedSerializer

    def get_serializer_class(self):
        return ApiRecipeSerializer if self.VERSION0 else ApiV1ExploreRecipeSerializer

    def get(self, request, *args, **kwargs):
        """
        Search recipes
        """
        chef = request.user
        action = kwargs['action']

        self.VERSION0 = request.path.startswith('/0/')
        hide_for_sale = self.VERSION0

        if action == 'explore':
            self.queryset = Recipes.objects.search_explore(chef, hide_for_sale=hide_for_sale)
        elif action == 'new':
            self.queryset = Recipes.objects.explore_recipes(chef, hide_for_sale=hide_for_sale)
        elif action == 'updated':
            date = request.GET.get('date')
            if not date:
                return self.invalid_request('Missing date field')
            date = str_to_datetime(date)
            self.queryset = Recipes.objects.search_updated(chef, date, hide_for_sale=hide_for_sale)
        elif action == 'search':
            query = request.GET.get('search')
            if not query:
                return self.invalid_request('Not search query string')

            fields = []
            if 'recipe' in request.GET:
                if request.GET['recipe'] == '1':
                    fields += ['recipe']

            if 'chef' in request.GET:
                if request.GET['chef'] == '1':
                    fields += ['chef']

            if 'book' in request.GET:
                if request.GET['book'] == '1':
                    fields += ['book']

            if 'ingredient' in request.GET:
                if request.GET['ingredient'] == '1':
                    fields += ['ingredient']

            if 'tags' in request.GET:
                if request.GET['tags'] == '1':
                    fields += ['tag']

            self.queryset = RecipeMapping.cookbooth_search(query, fields,
                                                           hide_for_sale=hide_for_sale)
            if self.queryset.count() == 0:
                raise Http404
        else:
            raise Http404

        return self.list(request, *args, **kwargs)

class RecipeDetailView(CookboothAPIView):

    def get(self, request, *args, **kwargs):

        if 'pk' not in kwargs:
            raise Http404()

        recipe_id = kwargs['pk']
        recipe_application_service = RecipeApplicationService.new()

        ingredient_subrecipe = recipe_application_service.get_ingredient_subrecipe_for_recipe(recipe_id)
        allergens = recipe_application_service.get_allergens_for_recipe(recipe_id)
        return Response({
            "ingredients": ingredient_subrecipe,
            "allergens": allergens
        })
