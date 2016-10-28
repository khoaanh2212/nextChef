from domain.costing.custom_changes_ingredient.CustomChangesIngredientService import CustomChangesIngredientService, \
    CustomChangesIngredient
from domain.costing.generic_ingredient.GenericIngredientService import GenericIngredientService
from domain.costing.CostingIngredientService import CostingIngredientService
from domain.costing.CostingIngredient import CostingIngredient
from django.conf import settings
import json


class CostingApplicationService:
    def __init__(self, generic_ingredient_service, custom_changes_ingredient_service, costing_ingredient_service):
        self.generic_ingredient_service = generic_ingredient_service
        self.custom_changes_ingredient_service = custom_changes_ingredient_service
        self.costing_ingredient_service = costing_ingredient_service

    def get_costing_table(self, chef, filter='', page=1):
        return map(lambda x: x.to_dto(), self.costing_ingredient_service.get_costing_table(chef, filter, page))

    def add_ingredient_row(self, ingredient, family, supplier, quantity, unit, gross_price, net_price, waste, comment):
        ingredient = self._mkIngredient(ingredient, family, supplier, quantity, unit, gross_price, net_price, waste,
                                        comment)
        return self.generic_ingredient_service.add_ingredient(ingredient).to_dto()

    def add_custom_ingredient_row(self, chef, ingredient, family, supplier, quantity, unit, gross_price, net_price,
                                  waste, comment):
        ingredient = self._mkIngredient(ingredient, family, supplier, quantity, unit, gross_price, net_price, waste,
                                        comment)
        custom_ingr = self.custom_changes_ingredient_service.add_custom_ingredient(chef, ingredient)
        return custom_ingr.to_dto()

    def edit_custom_ingredient_row(self, chef, custom_ingredient):
        ingredient = self._mkIngredient(custom_ingredient['ingredient'], custom_ingredient['family'],
                                        custom_ingredient['supplier'],
                                        custom_ingredient['quantity'], custom_ingredient['unit'],
                                        custom_ingredient['gross_price'] if custom_ingredient[
                                            'gross_price'] else 0, custom_ingredient['net_price'] if custom_ingredient[
                'net_price'] else 0, custom_ingredient['waste'] if custom_ingredient['waste'] else 0,
                                        custom_ingredient['comment'])
        custom_ingr = self.custom_changes_ingredient_service.update_custom_ingredient(custom_ingredient['id'], chef,
                                                                                      ingredient)
        return custom_ingr.to_dto()

    def edit_custom_ingredient_row_(self, custom_ingredient_id, chef, ingredient, family, supplier, quantity, unit,
                                    gross_price, net_price, waste, comment):
        ingredient = self._mkIngredient(ingredient, family, supplier, quantity, unit, gross_price, net_price, waste,
                                        comment)
        return self.custom_changes_ingredient_service.update_custom_ingredient(custom_ingredient_id, chef, ingredient)

    def edit_generic_custom_ingredient_row(self, chef, generic_ingredient):
        if not self.is_delete_generic_ingredient(chef, generic_ingredient):
            self.remove_custom_generic_ingredient_row(chef, generic_ingredient['generic_table_row_id'])

        return self.add_custom_ingredient_row(chef, generic_ingredient['ingredient'],
                                              generic_ingredient['family'],
                                              generic_ingredient['supplier'],
                                              generic_ingredient['quantity'],
                                              generic_ingredient['unit'], generic_ingredient['gross_price'],
                                              generic_ingredient['net_price'], generic_ingredient['waste'],
                                              generic_ingredient['comment'])

    def is_delete_generic_ingredient(self, chef, generic_ingredient):
        return CustomChangesIngredient.objects.filter(
            generic_table_row_id=generic_ingredient['generic_table_row_id'], is_deleted=True, chef_id=chef.id)

    def duplicate_custom_generic_ingredient_row(self, chef, generic_ingredient_id):
        generic_ingredient = self.generic_ingredient_service.get_by_id(generic_ingredient_id)
        ingredient = self._mkIngredient(generic_ingredient.ingredient, generic_ingredient.family,
                                        generic_ingredient.supplier, generic_ingredient.quantity,
                                        generic_ingredient.unit)

        custom_ingr = self.custom_changes_ingredient_service.add_custom_ingredient(chef, ingredient)
        return custom_ingr.to_dto()

    def duplicate_custom_ingredient_row(self, chef, ingredient_id):
        custom_ingredient = self.custom_changes_ingredient_service.get_by_id(ingredient_id)
        ingredient = self._mkIngredient(custom_ingredient.ingredient, custom_ingredient.family,
                                        custom_ingredient.supplier, custom_ingredient.quantity,
                                        custom_ingredient.unit, custom_ingredient.gross_price,
                                        custom_ingredient.net_price, custom_ingredient.waste,
                                        custom_ingredient.comment)

        custom_ingr = self.custom_changes_ingredient_service.add_custom_ingredient(chef, ingredient)
        return custom_ingr.to_dto()

    def remove_custom_generic_ingredient_row(self, chef, generic_ingredient_id):
        generic_ingredient = self.generic_ingredient_service.get_by_id(generic_ingredient_id)
        self.custom_changes_ingredient_service.remove_custom_generic_ingredient(chef, generic_ingredient)

    def remove_custom_ingredient_row(self, id):
        self.custom_changes_ingredient_service.remove_custom_ingredient(id)

    def _mkIngredient(self, ingredient, family, supplier, quantity, unit, gross_price=0, net_price=0, waste=0,
                      comment=''):
        return CostingIngredient(ingredient, family, quantity, unit, gross_price, waste, net_price, supplier, comment)

    def get_ingredient_suggestion_list(self, chef, filter, page):
        limit = settings.RECIPE_SUGGESTION_LIMIT
        total = self.costing_ingredient_service.count_suggestion_list(chef, filter)
        list = self.costing_ingredient_service.get_suggestion_list(chef, filter=filter, page=page)

        has_more = (page * limit) < total

        return {
            "total": total,
            "list": map(lambda x: x.to_dto(), list),
            "has_more": has_more
        }

    def _decorate_suggestion(self, suggestion_object):
        suggestion_object["list"] = map(lambda x: x.to_dto(), suggestion_object["list"])
        return suggestion_object

    @staticmethod
    def new(
            generic_ingredient_service=GenericIngredientService.new(),
            custom_changes_ingredient_service=CustomChangesIngredientService.new(),
            costing_ingredient_service=CostingIngredientService.new()
    ):
        return CostingApplicationService(generic_ingredient_service, custom_changes_ingredient_service,
                                         costing_ingredient_service)
