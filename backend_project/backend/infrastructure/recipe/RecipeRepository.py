from legacy_wrapper.recipe_wrapper import Recipe

from infrastructure.BaseRepository import BaseRepository

class RecipeRepository(BaseRepository):
    @staticmethod
    def new():
        return RecipeRepository(model=Recipe)

    def get_by_ids(self, ids):
        return self.model.objects.filter(draft=False, id__in=ids)\
            .order_by('-creation_date').order_by('name')

    def get_all_public(self, name):
        return self.model.objects\
            .filter(private=False, draft=False, name__icontains=name)\
            .order_by('-creation_date').order_by('name')

    def update_allergens_or_ingredient(self, recipe_id, allergens, ingredient):
        recipe = self.model.objects.get(id=recipe_id)
        recipe.pk = None
        recipe.allergens = allergens if allergens is not None else ''
        recipe.ingredients_order = ingredient if ingredient is not None else 'N;'
        recipe.save()
        return self.model.objects.filter(id=recipe_id).delete()

    def find_by_ids_for_explore(self, ids, chef=None):
        recipes = self.model.objects.filter(draft=False, id__in=ids)

        if chef and not chef.is_anonymous():
            recipes = recipes.exclude(chef__in=chef.following.all())
            recipes = recipes.exclude(pk__in=chef.recipes_added.all())
            recipes = recipes.exclude(chef=chef)

        recipes = recipes.select_related('chef').order_by('-final_score')
        return recipes
