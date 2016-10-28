from django.db import models
from model_utils.models import TimeStampedModel

from recipe.models import Recipes


class Product(TimeStampedModel):
    recipe = models.ManyToManyField(Recipes, related_name="products", blank=True)
    name = models.CharField('name', max_length=128)
    description = models.TextField('product description')
    price = models.CharField('price', max_length=20)
    shop_url = models.URLField('shop url', max_length=255)
    shop_title = models.CharField('shop title', max_length=128,  blank=True, null=True)
    barcode = models.CharField('barcode', max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'products'

    def __unicode__(self):
        return self.name


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, related_name="photos")
    photo = models.ImageField('photo', upload_to='products/photos/', blank=True)
    description = models.CharField('description', max_length=255, blank=True, null=True)
    order = models.SmallIntegerField('order')

    class Meta:
        db_table = 'product_images'

    def __unicode__(self):
        return self.photo.name

