from django.db import models


class CostingIngredientView(models.Model):

    id = models.CharField(primary_key=True, max_length=255)

    chef_id = models.IntegerField(blank=True)
    custom_id = models.IntegerField(blank=True)
    generic_table_row_id = models.IntegerField(blank=True, db_column='gen_id')
    deleted = models.TextField(blank=True)

    ingredient = models.CharField(max_length=255)
    family = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=255, blank=True)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, blank=True)
    gross_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    net_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    waste = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'costing_ingredient_view'

    def to_dto(self):
        return {
            'chef_id': get_id(self.chef_id),
            'custom_id': get_id(self.custom_id),
            'generic_table_row_id': get_id(self.generic_table_row_id),
            'ingredient': str(self.ingredient.encode('utf-8')),
            'family': str(self.family),
            'supplier': str(self.supplier),
            'quantity': float(self.quantity),
            'unit': str(self.unit),
            'gross_price': float(self.gross_price) if self.gross_price else None,
            'net_price': float(self.net_price) if self.net_price else None,
            'waste': int(self.waste) if self.waste else None,
        }

def get_id(id):
    try:
        return int(id)
    except Exception:
        return None
