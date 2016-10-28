from domain.recipe.RecipeService import RecipeService
from domain.recipe.edamam.EdamamService import EdamamService
from domain.book.BookService import BookService
from domain.costing.CostingIngredientService import CostingIngredientService
from domain.costing.generic_ingredient.GenericIngredientService import GenericIngredientService
from domain.costing.custom_changes_ingredient.CustomChangesIngredientService import CustomChangesIngredientService
from domain.recipe.RecipeHasIngredientService import RecipeHasIngredientService
from domain.recipe.RecipeHasSubrecipeService import RecipeHasSubrecipeService
from legacy_wrapper.recipe_wrapper import Recipe
from itertools import chain
from django.conf import settings
from infrastructure.recipe.RecipePermissionViewRepository import RecipePermissionViewRepository
from chefs.models import Chefs
from domain.costing.CostingIngredient import CostingIngredient
from domain.recipe.ingredient.Ingredient import Ingredient


class RecipeApplicationService:
    def __init__(
            self,
            recipe_service,
            edamam_service,
            book_service,
            costing_ingredient_service,
            generic_ingredient_service,
            custom_changes_ingredient_service,
            recipe_ingredient_service,
            recipe_subrecipe_service,
            recipe_wrapper,
            recipe_permission_view_repo
    ):
        self.recipe_service = recipe_service
        self.edamam_service = edamam_service
        self.book_service = book_service
        self.costing_ingredient_service = costing_ingredient_service
        self.generic_ingredient_service = generic_ingredient_service
        self.custom_changes_ingredient_service = custom_changes_ingredient_service
        self.recipe_ingredient_service = recipe_ingredient_service
        self.recipe_subrecipe_service = recipe_subrecipe_service
        self.recipe_wrapper = recipe_wrapper
        self.recipe_permission_view_repo = recipe_permission_view_repo

    def analyzeEdamam(self, recipe_ingredients):
        return self.edamam_service.getAllergens(recipe_ingredients)

    def get_recipe_by_books(self, books):
        recipes = self.book_service.get_recipe_by_books(books)
        return list(set(recipes))

    def get_recipe_by_chef(self, chef):
        return map(lambda x: Recipe(x).toDTO(), self.book_service.get_recipe_by_chef(chef))

    def get_recipe_in_public_books(self):
        return map(lambda x: self.recipe_wrapper(x).toDTO(), self.book_service.get_recipe_in_public_books())

    def get_recipe_by_following_chef(self, chef):
        return map(lambda x: self.recipe_wrapper(x).toDTO(), self.book_service.get_recipe_by_following_chef(chef))

    def get_all_public_recipes(self):
        recipes = self.recipe_permission_view_repo.find_public_recipe()
        ids = map(lambda x: x.recipe_id, list(recipes))
        return map(lambda x: self.recipe_wrapper(x).toDTO(), self.recipe_service.get_by_id(ids))

    def get_recipes_for_explore(self, chef):
        recipes = self.recipe_permission_view_repo.find_public_recipe()
        ids = map(lambda x: x.recipe_id, list(recipes))
        return self.recipe_service.get_by_ids_for_explore(ids, chef)

    def is_recipe_available_for_chef(self, recipe_id, chef_id):
        return self.recipe_permission_view_repo.is_recipe_available_for_chef(recipe_id=recipe_id, chef_id=chef_id)

    def get_visible_recipes(self, current_user_id, homepage_user_id):
        recipes = self.recipe_permission_view_repo.find_visible_recipes(current_user_id, homepage_user_id)
        ids = map(lambda x: x.recipe_id, list(recipes))
        return self.recipe_service.get_by_id(ids)

    def verify_ingredient(self, text):
        return self.edamam_service.verify_ingredient(text)

    def add_ingredient(self, recipe_id, costing_ingredient_id, is_custom, text, chef=Chefs):
        recipe = self.recipe_service.get_by_id(recipe_id).to_instance()
        if isinstance(costing_ingredient_id, int):
            if is_custom:
                costing_ingredient = self.custom_changes_ingredient_service.get_by_id(costing_ingredient_id)
            else:
                costing_ingredient = self.generic_ingredient_service.get_by_id(costing_ingredient_id)
            text = text + ' ' + costing_ingredient.ingredient
        else:
            text = text + ' ' + costing_ingredient_id

        ingredient = self.verify_ingredient(text)
        if not isinstance(costing_ingredient_id, int):
            costing_ingredient = self.add_new_ingredient_into_custom_ingredient(costing_ingredient_id, chef)

        order = self.getBigestOrder(recipe_id)
        return self.recipe_ingredient_service.add(recipe, costing_ingredient, ingredient, order)

    def add_ingredient_without_verified_edamam(self, recipe_id, costing_ingredient_id, is_custom, text, chef=Chefs):
        recipe = self.recipe_service.get_by_id(recipe_id).to_instance()
        if isinstance(costing_ingredient_id, int):
            if is_custom:
                costing_ingredient = self.custom_changes_ingredient_service.get_by_id(costing_ingredient_id)
            else:
                costing_ingredient = self.generic_ingredient_service.get_by_id(costing_ingredient_id)

        if not isinstance(costing_ingredient_id, int):
            costing_ingredient = self.add_new_ingredient_into_custom_ingredient(costing_ingredient_id, chef)

        amount = self.handle_amout_ingredient(text)
        measure = self.hand_measure_ingredient(text)
        order = self.getBigestOrder(recipe_id)

        ingredient = self.init_ingredient_to_add_to_recipe_without_verify_edamam(amount, measure, costing_ingredient)
        return self.recipe_ingredient_service.addWithoutVerifyEdamam(recipe, costing_ingredient, ingredient, order)

    def init_ingredient_to_add_to_recipe_without_verify_edamam(self, amount, measure, costing_ingredient):
        text = amount + ' ' + measure + ' ' + costing_ingredient.ingredient
        quantity = float(amount)
        if measure == 'kg':
            weight_in_gr = quantity * 1000
        elif measure == 'lbs':
            weight_in_gr = quantity * 453.59
        else:
            weight_in_gr = 0

        ingredient = Ingredient(text, weight_in_gr, measure, quantity)
        return ingredient

    def handle_amout_ingredient(self, amount):
        arrAmount = amount.split(' ', 1)
        if not self.RepresentFloat(arrAmount[0]):
            arrAmount[0] = '1'
        return arrAmount[0]

    def hand_measure_ingredient(self, strText):
        arrText = strText.split(' ')
        if len(arrText) < 2:
            return ''
        else:
            strReturn = ''
            for i in range(1, len(arrText)):
                if strReturn == '':
                    strReturn = strReturn + arrText[i]
                else:
                    strReturn = strReturn + ' ' + arrText[i]
            return strReturn
        return ''

    def RepresentFloat(self, str):
        try:
            float(str)
            return True
        except:
            return False

    def add_new_ingredient_into_custom_ingredient(self, ingredientName, chef):
        costingIngredient = CostingIngredient(ingredientName)
        return self.custom_changes_ingredient_service.add_custom_ingredient(chef, costingIngredient)

    def delete_ingredient(self, id):
        return self.recipe_ingredient_service.delete(id)

    def get_ingredient_subrecipe_for_recipe(self, recipe_id):
        ingredients = self.recipe_ingredient_service.get_by_recipe_id(recipe_id)
        subrecipes = self.recipe_subrecipe_service.get_by_recipe_id(recipe_id)
        result = list(chain(ingredients, subrecipes))
        recipeService = RecipeService.new()
        result = recipeService.sort_ingredients(result)
        return map(lambda x: x.to_dto(), result)

    def getBigestOrder(self, recipeId):
        bigestOrderIngredient = self.recipe_ingredient_service.getBigestOrder(recipeId)
        bigestOrderSubRecipe = self.recipe_subrecipe_service.getBigestOrder(recipeId)
        return (bigestOrderIngredient + 1) if (bigestOrderIngredient > bigestOrderSubRecipe) else (
            bigestOrderSubRecipe + 1)

    def get_allergens_for_recipe(self, recipe_id):
        ingredients = self.recipe_ingredient_service.get_by_recipe_id(recipe_id)
        subrecipes = self.recipe_subrecipe_service.get_by_recipe_id(recipe_id)
        recipe = self.recipe_service.get_by_id(recipe_id)
        result = list(chain(ingredients, subrecipes, [recipe]))
        return self._extract_allergens(map(lambda x: x.to_dto()['allergens'], result))

    def _extract_allergens(self, allergens):
        allergen_list = []

        for allergen in allergens:
            allergen_list.extend(allergen.split(','))

        allergen_list = map(lambda x: x.strip(), allergen_list)
        return sorted(list(set(allergen_list)))

    def add_subrecipe(self, recipe_id, subrecipe_id, amount):
        recipe = self.recipe_service.get_by_id(recipe_id).to_instance()
        subrecipe = self.recipe_service.get_by_id(subrecipe_id).to_instance()
        price = self.recipe_ingredient_service.get_price(subrecipe.id) + \
                self.recipe_subrecipe_service.get_price(subrecipe.id)

        allergen_list = self.get_allergens_for_recipe(subrecipe_id)
        order = self.getBigestOrder(recipe_id)
        return self.recipe_subrecipe_service.create(recipe, subrecipe, price, allergen_list, order, amount)

    def delete_subrecipe(self, id):
        return self.recipe_subrecipe_service.delete(id)

    def add_custom_allergens(self, recipe_id, allergens):
        return self.recipe_service.add_allergens_to_recipe(recipe_id, allergens)

    def remove_custom_allergens(self, recipe_id, allergens):
        self.recipe_service.remove_allergens_from_recipe(recipe_id, allergens)
        self.recipe_ingredient_service.remove_allergens(recipe_id, allergens)
        self.recipe_subrecipe_service.remove_allergens(recipe_id, allergens)

    def get_recipe_suggestion_list(self, chef, filter, page):

        limit = settings.RECIPE_SUGGESTION_LIMIT
        total = self.recipe_service.count_suggestion_list(chef, filter)
        list = self.recipe_service.get_suggestion_list(chef, filter=filter, page=page)

        has_more = (page * limit) < total

        return {
            "total": total,
            "list": map(lambda x: x.to_dto(), list),
            "has_more": has_more
        }

    @staticmethod
    def new(
            recipe_service=RecipeService.new(),
            edamam_service=EdamamService.new(),
            book_service=BookService.new(),
            costing_ingredient_service=CostingIngredientService.new(),
            generic_ingredient_service=GenericIngredientService.new(),
            custom_changes_ingredient_service=CustomChangesIngredientService.new(),
            recipe_ingredient_service=RecipeHasIngredientService.new(),
            recipe_subrecipe_service=RecipeHasSubrecipeService.new(),
            recipe_wrapper=Recipe,
            recipe_permission_view_repo=RecipePermissionViewRepository.new()
    ):
        return RecipeApplicationService(recipe_service, edamam_service, book_service, costing_ingredient_service,
                                        generic_ingredient_service, custom_changes_ingredient_service,
                                        recipe_ingredient_service, recipe_subrecipe_service, recipe_wrapper,
                                        recipe_permission_view_repo)

    def get_price_and_allergen(self, recipe):
        price = self.costing_ingredient_service.get_by_recipe_id(recipe.id).gross_price
        allergens = self.recipe_service.get_by_id(recipe.id).allergens
        return {
            'price': price,
            'allergens': allergens
        }
