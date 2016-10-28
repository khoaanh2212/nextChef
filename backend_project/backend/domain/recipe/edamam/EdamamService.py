from infrastructure.recipe.EdamamRepository import EdamamRepository
from .Edamam import Edamam
from domain.recipe.ingredient.Ingredient import Ingredient
from infrastructure.recipe.EdamamGateway import EdamamGateway
import json


class EdamamService:
    def __init__(self, repository, model, edamam_gateway):
        self.repository = repository
        self.model = model
        self.edamam_gateway = edamam_gateway

    def getAllergens(self, recipe_ingredients):
        request = self._decorateIngredients(recipe_ingredients)
        edamam_response = self.edamam_gateway.getAllergens(request)

        if not edamam_response['cached']:
            self.repository.save(self.model.create(request, edamam_response['response']))

        return edamam_response['allergens']

    def verify_ingredient(self, text):
        ingredient = Ingredient(text)
        return self.edamam_gateway.verify_ingredient(ingredient)

    def _decorateIngredients(self, recipe_ingredients):
        return {'ingr': recipe_ingredients}

    @staticmethod
    def new(repository = EdamamRepository.new(), model = Edamam, edamam_gateway = EdamamGateway.new()):
        return EdamamService(repository, model, edamam_gateway)
