from django.db import models
from recipe.models import Recipes
from domain.PositiveFloatNumber import PositiveFloatNumber
from domain.recipe.SelectedAllergens import SelectedAllergens


class InvalidRecipeHasSubrecipeArgumentException(Exception):
    pass


class RecipeHasSubrecipe(models.Model):
    r_id = models.IntegerField()
    sr_id = models.IntegerField()
    sr_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    sr_allergens = models.TextField(blank=True)
    sr_name = models.CharField(max_length=255, blank=True)
    sr_owner_name = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(max_length=8, default=0)
    amount = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'recipe_has_subrecipe'

    @classmethod
    def create(cls, recipe, sub_recipe, sub_recipe_price, subrecipe_allergens, order, amount):

        if not isinstance(recipe, Recipes):
            raise InvalidRecipeHasSubrecipeArgumentException

        if not isinstance(sub_recipe, Recipes):
            raise InvalidRecipeHasSubrecipeArgumentException

        if recipe.id == sub_recipe.id:
            raise InvalidRecipeHasSubrecipeArgumentException

        if not isinstance(subrecipe_allergens, SelectedAllergens):
            raise InvalidRecipeHasSubrecipeArgumentException

        sr_name = sub_recipe.name
        sr_owner_name = sub_recipe.chef.name + " " + sub_recipe.chef.surname

        return cls(
            r_id=recipe.id,
            sr_id=sub_recipe.id,
            sr_price=PositiveFloatNumber(sub_recipe_price).number,
            sr_allergens=subrecipe_allergens.toAllergenString(),
            sr_name=sr_name,
            sr_owner_name=sr_owner_name,
            order=order,
            amount=amount
        )

    def to_dto(self):
        return {
            "type": "recipe",
            "id": self.id,
            "recipe_id": self.r_id,
            "subrecipe_id": self.sr_id,
            "price": self.sr_price,
            "allergens": self.sr_allergens,
            "name": self.sr_name,
            "owner_name": self.sr_owner_name,
            "order": self.order,
            "amount": self.amount
        }

    def set_allergens(self, selected_allergens):
        self.sr_allergens = selected_allergens.toAllergenString()
