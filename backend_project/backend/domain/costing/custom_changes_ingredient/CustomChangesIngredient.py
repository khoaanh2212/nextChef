from django.db import models

from chefs.models import Chefs
from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from domain.costing.CostingIngredient import CostingIngredient


class CustomChangesIngredient(models.Model):
    UNIT_KG = 'kg'
    UNIT_LBS = 'lbs'

    UNIT_CHOICES = (
        (UNIT_KG, 'kilogram'), (UNIT_LBS, 'pound')
    )

    generic_table_row_id = models.IntegerField(default=0)
    chef_id = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    ingredient = models.CharField(max_length=255)
    family = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=255, blank=True)

    quantity = models.DecimalField(default=1, max_digits=11, decimal_places=3)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_KG)
    gross_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    net_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    waste = models.IntegerField(default=0)

    comment = models.TextField(blank=True)

    class Meta:
        db_table = 'custom_changes_ingredient'

    @classmethod
    def create(cls, chef, costing_ingredient):

        if not isinstance(costing_ingredient, CostingIngredient):
            raise InvalidIngredient

        if not isinstance(chef, Chefs):
            raise InvalidChef

        return cls(
            chef_id=chef.id,
            ingredient=costing_ingredient.ingredient,
            family=costing_ingredient.family,
            supplier=costing_ingredient.supplier,
            quantity=costing_ingredient.quantity,
            unit=costing_ingredient.unit,
            gross_price=costing_ingredient.gross_price,
            net_price=costing_ingredient.net_price,
            waste=costing_ingredient.waste,
            comment=costing_ingredient.comment,
        )

    @classmethod
    def remove(cls, chef, generic_ingredient):

        if not isinstance(generic_ingredient, GenericIngredient):
            raise InvalidIngredient
        if not isinstance(chef, Chefs):
            raise InvalidChef

        return cls(
            chef_id=chef.id,
            generic_table_row_id=generic_ingredient.id,

            ingredient=generic_ingredient.ingredient,
            family=generic_ingredient.family,
            supplier=generic_ingredient.supplier,
            quantity=generic_ingredient.quantity,
            unit=generic_ingredient.unit,

            is_deleted=True
        )

    def to_dto(self):
        return {
            "id": self.id,
            "genericTableRowId": self.generic_table_row_id,
            "chefId": self.chef_id,
            "ingredient": self.ingredient,
            "family": self.family,
            "supplier": self.supplier,
            "quantity": self.quantity,
            "unit": self.unit,
            "grossPrice": self.gross_price,
            "netPrice": self.net_price,
            "waste": self.waste
        }


class InvalidCustomChangesIngredientModelArgumentException(Exception):
    pass


class InvalidIngredient(InvalidCustomChangesIngredientModelArgumentException):
    pass


class InvalidChef(InvalidCustomChangesIngredientModelArgumentException):
    pass
