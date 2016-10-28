from django.db import models
from domain.costing.CostingIngredient import CostingIngredient


class InvalidGenericIngredientException(Exception):
    pass


class GenericIngredient(models.Model):

    UNIT_KG = 'kg'
    UNIT_LBS = 'lbs'

    UNIT_CHOICES = (
        (UNIT_KG, 'kilogram'), (UNIT_LBS, 'pound')
    )

    ingredient = models.CharField(max_length=255)
    family = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=255, blank=True)

    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_KG)
    # gross_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    # net_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    # waste = models.IntegerField(default=0)

    class Meta:
        db_table = 'generic_ingredient'

    @classmethod
    def create(cls, costing_ingredient):

        if not isinstance(costing_ingredient, CostingIngredient):
            raise InvalidGenericIngredientException

        return cls(
            ingredient=costing_ingredient.ingredient,
            family=costing_ingredient.family,
            supplier=costing_ingredient.supplier,
            quantity=costing_ingredient.quantity,
            unit=costing_ingredient.unit,
            # gross_price=costing_ingredient.gross_price,
            # net_price=costing_ingredient.net_price,
            # waste=costing_ingredient.waste
        )

    def to_dto(self):
        return {
            'id': self.id,
            'ingredient': self.ingredient,
            'family': self.family,
            'supplier': self.supplier,
            'quantity': self.quantity,
            'unit': self.unit,
            # 'gross_price': self.gross_price,
            # 'net_price': self.net_price,
            # 'waste': self.waste
        }
