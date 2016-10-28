from infrastructure.costing.custom_changes_ingredient.CustomChangesIngredientRepository import CustomChangesIngredientRepository
from .CustomChangesIngredient import CustomChangesIngredient


class InvalidCustomChangesIngredientArgumentException(Exception):
    pass


class CustomChangesIngredientService:

    def __init__(self, model, repository):
        self.model = model
        self.repository = repository

    def add_custom_ingredient(self, chef, ingredient):
        return self.repository.save(self.model.create(chef, ingredient))

    def update_custom_ingredient(self, ingredient_id, chef, ingredient):
        instance = self.model.create(chef, ingredient)
        instance.id = ingredient_id
        return self.repository.save(instance)

    def remove_custom_generic_ingredient(self, chef, generic_ingredient):
        return self.repository.save(self.model.remove(chef, generic_ingredient))

    def remove_custom_ingredient(self, id):
        try:
            self.repository.remove(id)
        except CustomChangesIngredient.DoesNotExist:
            raise InvalidCustomChangesIngredientArgumentException

    def get_by_id(self, id):
        try:
            return self.repository.findById(id)
        except CustomChangesIngredient.DoesNotExist:
            raise InvalidCustomChangesIngredientArgumentException

    @staticmethod
    def new(model = CustomChangesIngredient, repository = CustomChangesIngredientRepository.new()):
        return CustomChangesIngredientService(model, repository)
