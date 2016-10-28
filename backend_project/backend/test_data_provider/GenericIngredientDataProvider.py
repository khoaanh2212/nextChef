from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from domain.costing.CostingIngredient import CostingIngredient


class GenericIngredientDataProvider:

    def __init__(self):

        costing_ingredient = CostingIngredient('Ingredient')

        self.costing = GenericIngredient.create(
            costing_ingredient=costing_ingredient
        )

    @staticmethod
    def get():
        return GenericIngredientDataProvider()

    def withIngredient(self, ingredient):
        self.costing.ingredient = ingredient
        return self

    def withFamily(self, family):
        self.costing.family = family
        return self

    def withSupplier(self, supplier):
        self.costing.supplier = supplier
        return self

    def with_id(self, id):
        self.costing.id = id
        return self

    def with_net_price(self, net_price):
        self.costing.net_price = net_price
        return self

    def with_unit(self, unit):
        self.costing.unit = unit
        return self

    def build(self):
        return self.costing

    @staticmethod
    def getDefault():
        costing = GenericIngredientDataProvider()
        return costing.build()
