from infrastructure.recipe.RecipeRepository import RecipeRepository
from infrastructure.recipe.RecipeSuggestionViewRepository import RecipeSuggestionViewRepository
from domain.recipe.SelectedAllergens import SelectedAllergens, Allergen
from django.conf import settings


class RecipeService:
    def __init__(self, repository, recipe_suggestion_view_repository):
        self.repository = repository
        self.recipe_suggestion_view_repository = recipe_suggestion_view_repository

    @staticmethod
    def new(
            repository=RecipeRepository.new(),
            recipe_suggestion_view_repository=RecipeSuggestionViewRepository.new()
    ):
        return RecipeService(repository, recipe_suggestion_view_repository)

    def get_by_id(self, recipe_id):
        return self.repository.findById(recipe_id)

    def get_by_ids_for_explore(self, ids, chef):
        return self.repository.find_by_ids_for_explore(ids, chef)

    def add_allergens_to_recipe(self, recipe_id, allergens):
        recipe = self.repository.findById(recipe_id)
        previous_allergens = recipe.model.allergens.split(',')
        allergen_instance = SelectedAllergens.new(previous_allergens)

        for allergen in allergens:
            allergen_instance.add(Allergen(allergen.strip()))

        recipe.set_allergens(allergen_instance)
        self.repository.save(recipe)
        return recipe.to_instance()

    def remove_allergens_from_recipe(self, recipe_id, allergens):
        recipe = self.repository.findById(recipe_id)
        previous_allergens = recipe.model.allergens.split(',')
        allergen_instance = SelectedAllergens.new(previous_allergens)

        for allergen in allergens:
            print(allergen)
            allergen_instance.remove(Allergen(allergen.strip()))

        recipe.set_allergens(allergen_instance)
        self.repository.save(recipe)
        return recipe.to_instance()

    def get_suggestion_list(self, chef, filter, page):
        return self.recipe_suggestion_view_repository.find_by_chef(chef, filter=filter, page=page)

    def count_suggestion_list(self, chef, filter):
        return self.recipe_suggestion_view_repository.count_by_chef(chef, filter=filter)

    def sort_ingredients(self, listIngredient):
        for ingredient in range(len(listIngredient) - 1, 0, -1):
            for i in range(ingredient):
                if (listIngredient[i].order > listIngredient[i + 1].order):
                    temp = listIngredient[i]
                    listIngredient[i] = listIngredient[i + 1]
                    listIngredient[i + 1] = temp
        return listIngredient
