from domain.recipe.RecipeHasSubrecipe import RecipeHasSubrecipe
import copy


class RecipeHasSubrecipeDataProvider:
    def __init__(self, recipe_has_subrecipe=RecipeHasSubrecipe(
    )):
        self.recipe_has_subrecipe = copy.deepcopy(recipe_has_subrecipe)

    def build(self):
        if not self.recipe_has_subrecipe.sr_id:
            self.recipe_has_subrecipe.sr_id = 10
        return self.recipe_has_subrecipe

    def with_recipe_id(self, recipe_id):
        self.recipe_has_subrecipe.r_id = recipe_id
        return self

    def with_price(self, price):
        self.recipe_has_subrecipe.sr_price = price
        return self

    def with_allergens(self, allergens):
        self.recipe_has_subrecipe.sr_allergens = allergens
        return self

    def with_order(self, order):
        self.recipe_has_subrecipe.order = order
        return self

    @staticmethod
    def get():
        return RecipeHasSubrecipeDataProvider()

    @staticmethod
    def get_default():
        data_provider = RecipeHasSubrecipeDataProvider()
        return data_provider.build()
