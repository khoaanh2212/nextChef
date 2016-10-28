from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from infrastructure.BaseRepository import BaseRepository


class CustomChangesIngredientRepository(BaseRepository):

    @staticmethod
    def new():
        return CustomChangesIngredientRepository(model=CustomChangesIngredient)

    def remove(self, id):
        self.model.objects.get(id=id).delete()
