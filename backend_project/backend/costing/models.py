# from django.db import models
#
#
# # Create your models here.
#
# class GenericIngredient(models.Model):
#     UNIT_KG = 'kg'
#     UNIT_LBS = 'lbs'
#
#     UNIT_CHOICES = (
#         (UNIT_KG, 'kilogram'), (UNIT_LBS, 'pound')
#     )
#
#     ingredient = models.CharField(max_length=255)
#     family = models.CharField(max_length=255, blank=True)
#     supplier = models.CharField(max_length=255, blank=True)
#
#     quantity = models.IntegerField(default=1)
#     unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_KG)
#
#     # gross_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#     # net_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#     # waste = models.IntegerField(default=0)
#
#     class Meta:
#         db_table = 'generic_ingredient'
#
#
# class CustomChangesIngredient(models.Model):
#     UNIT_KG = 'kg'
#     UNIT_LBS = 'lbs'
#
#     UNIT_CHOICES = (
#         (UNIT_KG, 'kilogram'), (UNIT_LBS, 'pound')
#     )
#
#     generic_table_row_id = models.IntegerField(default=0)
#     chef_id = models.IntegerField()
#     is_deleted = models.BooleanField(default=False)
#
#     ingredient = models.CharField(max_length=255)
#     family = models.CharField(max_length=255, blank=True)
#     supplier = models.CharField(max_length=255, blank=True)
#
#     quantity = models.DecimalField(default=1, max_digits=11, decimal_places=3)
#     unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_KG)
#     gross_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#     net_price = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#     waste = models.IntegerField(default=0)
#
#     comment = models.TextField(blank=True)
#
#     class Meta:
#         db_table = 'custom_changes_ingredient'
