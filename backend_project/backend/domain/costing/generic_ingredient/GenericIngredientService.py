from infrastructure.costing.generic_ingredient.GenericIngredientRepository import GenericIngredientRepository
from .GenericIngredient import GenericIngredient


class InvalidGenericIngredientArgumentException(Exception):
    pass


class GenericIngredientService:

    def __init__(self, model, repository):
        self.model = model
        self.repository = repository

    def getAll(self, filter='', page=1):
        return self.repository.findAll(filter=filter, page=page)

    def get_by_id(self, id):
        try:
            return self.repository.findById(id)
        except GenericIngredient.DoesNotExist:
            raise InvalidGenericIngredientArgumentException

    def add_ingredient(self, ingredient):
        return self.repository.save(self.model.create(ingredient))

    @staticmethod
    def new(model = GenericIngredient, repository = GenericIngredientRepository.new()):
        return GenericIngredientService(model, repository)