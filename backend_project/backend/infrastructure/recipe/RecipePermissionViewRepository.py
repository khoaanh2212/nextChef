from django.conf import settings
from django.db.models import Q
from infrastructure.BaseRepository import BaseRepository
from domain.recipe.RecipePermissionView import RecipePermissionView


class RecipePermissionViewRepository(BaseRepository):
    @staticmethod
    def new():
        return RecipePermissionViewRepository(model=RecipePermissionView)

    def find_public_recipe(self):
        return self.model.objects.filter(state='public')

    def is_recipe_available_for_chef(self, recipe_id, chef_id):
        if not chef_id:
            result = self.model.objects.filter(Q(recipe_id=recipe_id) & Q(state='public'))
        else:
            collaborator_keyword = '[%d]' % chef_id

            result = self.model.objects.filter(
                Q(recipe_id=recipe_id) &
                (
                    Q(state='public') |
                    Q(recipe_chef_id=chef_id) |
                    Q(collaborators__contains=collaborator_keyword)
                )
            )

        return len(result) > 0

    def find_visible_recipes(self, current_user_id, homepage_user_id):
        homepage_collaborator_keyword = '[%d]' % homepage_user_id
        current_collaborator_keyword = '[%d]' % current_user_id

        recipes = self.model.objects.filter(
            (
                Q(recipe_chef_id=homepage_user_id) |
                Q(collaborators__contains=homepage_collaborator_keyword) |
                Q(book_chef_id=homepage_user_id)
            ) &
            (
                Q(state='public') |
                Q(recipe_chef_id=current_user_id) |
                Q(collaborators__contains=current_collaborator_keyword)
            )
        )

        return recipes
