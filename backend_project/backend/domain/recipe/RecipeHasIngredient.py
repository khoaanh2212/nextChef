from django.db import models
from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from recipe.models import Recipes
from domain.recipe.ingredient.Ingredient import Ingredient
from django.conf import settings
from decimal import Decimal


class InvalidRecipeHasIngredientArgumentException(Exception):
    pass


class InvalidRecipeException(InvalidRecipeHasIngredientArgumentException):
    pass


class InvalidIngredientException(InvalidRecipeHasIngredientArgumentException):
    pass


class InvalidEdamamIngredientException(InvalidRecipeHasIngredientArgumentException):
    pass


class RecipeHasIngredient(models.Model):
    recipe_id = models.IntegerField()
    text = models.TextField(blank=True)
    custom_ingredient_id = models.IntegerField(blank=True)
    generic_ingredient_id = models.IntegerField(blank=True)
    measure = models.CharField(max_length=255, blank=True)
    quantity = models.DecimalField(max_digits=11, decimal_places=3, default=0)
    weight_in_gr = models.DecimalField(max_digits=14, decimal_places=3, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, blank=True)
    allergens = models.TextField(blank=True)
    ingredient_name = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(max_length=8, default=0)

    class Meta:
        db_table = 'recipe_has_ingredient'

    @classmethod
    def create(cls, recipe, costing_ingredient, edamam_ingredient, order):

        if not isinstance(recipe, Recipes):
            raise InvalidRecipeException

        if not isinstance(edamam_ingredient, Ingredient):
            raise InvalidEdamamIngredientException

        generic_ingredient_id = 0
        custom_ingredient_id = 0

        if isinstance(costing_ingredient, GenericIngredient):
            generic_ingredient_id = costing_ingredient.id
        elif isinstance(costing_ingredient, CustomChangesIngredient):
            custom_ingredient_id = costing_ingredient.id
        else:
            raise InvalidIngredientException

        instance = cls(
            recipe_id=recipe.id,
            text=edamam_ingredient.text,
            measure=edamam_ingredient.measure,
            quantity=edamam_ingredient.quantity,
            weight_in_gr=edamam_ingredient.weight_in_gr,
            price=calculate_price(edamam_ingredient, costing_ingredient) if custom_ingredient_id != 0 else None,
            allergens=edamam_ingredient.allergens.to_allergen_string(),
            generic_ingredient_id=generic_ingredient_id,
            custom_ingredient_id=custom_ingredient_id,
            ingredient_name=costing_ingredient.ingredient,
            order = order
        )

        return instance

    @classmethod
    def createWithoutVerifyEdamam(cls, recipe, costing_ingredient, edamam_ingredient, order):

        if not isinstance(recipe, Recipes):
            raise InvalidRecipeException

        if not isinstance(edamam_ingredient, Ingredient):
            raise InvalidEdamamIngredientException

        generic_ingredient_id = 0
        custom_ingredient_id = 0

        if isinstance(costing_ingredient, GenericIngredient):
            generic_ingredient_id = costing_ingredient.id
        elif isinstance(costing_ingredient, CustomChangesIngredient):
            custom_ingredient_id = costing_ingredient.id
        else:
            raise InvalidIngredientException

        instance = cls(
            recipe_id=recipe.id,
            text=edamam_ingredient.text,
            measure=edamam_ingredient.measure,
            quantity=edamam_ingredient.quantity,
            weight_in_gr=edamam_ingredient.weight_in_gr,
            price=calculate_price(edamam_ingredient, costing_ingredient) if custom_ingredient_id != 0 else None,
            allergens='',
            generic_ingredient_id=generic_ingredient_id,
            custom_ingredient_id=custom_ingredient_id,
            ingredient_name=costing_ingredient.ingredient,
            order=order
        )

        return instance

    def to_dto(self):
        return {
            "type": "ingredient",
            "id": self.id,
            "recipe_id": self.recipe_id,
            "text": self.text,
            "measure": self.measure,
            "quantity": self.quantity,
            "weight_in_gr": self.weight_in_gr,
            "price": self.price,
            "allergens": self.allergens,
            "generic_ingredient_id": self.generic_ingredient_id,
            "custom_ingredient_id": self.custom_ingredient_id,
            "name": self.ingredient_name,
            "order": self.order
        }

    def set_allergens(self, selected_allergens):
        self.allergens = selected_allergens.toAllergenString()


def calculate_price(edamam_ingredient, costing_ingredient):
    weight = edamam_ingredient.weight_in_gr * settings.GR_TO_KG
    if costing_ingredient.unit is settings.UNIT_LBS:
        weight = weight * settings.KG_TO_LBS
    price = Decimal(costing_ingredient.gross_price/costing_ingredient.quantity) * Decimal(weight)
    return round(price, 2)
