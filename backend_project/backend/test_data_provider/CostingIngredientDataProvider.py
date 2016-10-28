from domain.costing.CostingIngredient import CostingIngredient


class CostingIngredientDataProvider:

    def __init__(self):
        self.instance = CostingIngredient('Ingredient')

    @staticmethod
    def get():
        return CostingIngredientDataProvider()

    def with_ingredient(self, ingredient):
        self.instance.ingredient = ingredient
        return self

    def build(self):
        return self.instance

    @staticmethod
    def get_default():
        instance = CostingIngredientDataProvider()
        return instance.build()
