from django.db import models
from recipe.models import Recipes


class Subscriber(models.Model):
    name = models.CharField(max_length=200, blank=False)
    token = models.CharField(max_length=50, blank=False)   
    is_active = models.BooleanField(default=False) 
    
    def __unicode__(self):
        return self.name
    
    
class SubscriptionRecipe(models.Model):
    recipe = models.ForeignKey(Recipes, blank=False)
    subscriber = models.ForeignKey(Subscriber, blank=False)
    date = models.DateField(blank=False)