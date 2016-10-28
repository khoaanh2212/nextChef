from recipe.models import Recipes
import copy


class RecipeDataProvider:
    def __init__(self, recipe = Recipes()):
        self.recipe = copy.deepcopy(recipe)
        self.recipe.private = True

    def build(self):
        return self.recipe

    def with_id(self, id):
        self.recipe.id = id
        return self

    def with_name(self, name):
        self.recipe.name = name
        return self

    def with_chef(self, chef):
        self.recipe.chef = chef
        return self

    def with_allergens(self, allergens):
        self.recipe.allergens = allergens
        return self

    def active(self):
        self.recipe.draft = False
        return self

    def publish(self):
        self.recipe.private = False
        return self

    @staticmethod
    def get():
        return RecipeDataProvider()

    @staticmethod
    def get_default():
        data_provider = RecipeDataProvider()
        return data_provider.build()
