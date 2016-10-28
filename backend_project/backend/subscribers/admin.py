from django.contrib import admin

from django.db.models import get_model
from .models import Subscriber, SubscriptionRecipe

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'is_active')
    search_fields = ('name',)
    #filter_horizontal = ('is_active',)

admin.site.register(Subscriber, SubscriberAdmin)

class SubscriptionRecipeAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'recipe', 'date',)
    search_fields = ('subscriber', 'recipe',)
    #filter_horizontal = ('subscriber',)
    raw_id_fields = ('recipe',)
    related_lookup_fields = {
        'm2m': ['recipes']
    }
    
admin.site.register(SubscriptionRecipe, SubscriptionRecipeAdmin)
