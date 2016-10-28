
from django.template import defaultfilters
from django.db import models

from recipe.models import Recipes

class CollectionRecipes(models.Model):
    recipe = models.ForeignKey(Recipes, db_column="recipes_id")
    collection = models.ForeignKey('Collection', db_column="collection_id")
    score = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        db_table = 'colls_collection_recipes'
        unique_together = ('recipe', 'collection')
        ordering = ['score',]

class Collection(models.Model):
    name = models.CharField(max_length=32, blank=False)
    title1 = models.CharField(max_length=16, blank=False)
    title2 = models.CharField(max_length=16, blank=False)
    description = models.TextField(blank=False, default='')
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=False)
    recipes = models.ManyToManyField(Recipes, blank=True, through=CollectionRecipes)
    cover = models.ImageField('image', upload_to='collections/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Collection, self).save(*args, **kwargs)


