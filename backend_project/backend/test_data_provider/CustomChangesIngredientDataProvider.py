from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from .ChefDataProvider import ChefDataProvider
from domain.costing.CostingIngredient import CostingIngredient


class CustomChangesIngredientDataProvider:

    def __init__(self):

        costing_ingredient = CostingIngredient('Ingredient')

        self.instance = CustomChangesIngredient.create(
            chef=ChefDataProvider.get().withId(1).build(),
            costing_ingredient=costing_ingredient
        )

    @staticmethod
    def get():
        return CustomChangesIngredientDataProvider()

    def with_ingredient(self, ingredient):
        self.instance.ingredient = ingredient
        return self

    def with_chef_id(self, chef_id):
        self.instance.chef_id = chef_id
        return self

    def with_net_price(self, net_price):
        self.instance.net_price = net_price
        return self

    def with_gross_price(self,gross_price):
        self.instance.gross_price = gross_price
        return self

    def with_is_deleted(self, is_deleted):
        self.instance.is_deleted = is_deleted
        return self

    def with_unit(self, unit):
        self.instance.unit = unit
        return self

    def with_generic_ingredient_id(self, generic_ingredient_id):
        self.instance.generic_table_row_id = generic_ingredient_id
        return self

    def with_id(self, id):
        self.instance.id = id
        return self

    def build(self):
        return self.instance

    @staticmethod
    def get_default():
        instance = CustomChangesIngredientDataProvider()
        return instance.build()
