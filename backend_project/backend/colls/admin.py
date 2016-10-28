from django.contrib import admin

from .models import Collection, CollectionRecipes


class CollectionRecipeInline(admin.TabularInline):
    model = CollectionRecipes
    fields = ('recipe','score',)
    extra = 0
    raw_id_fields = ('recipe',)
    related_lookup_fields = {
        'm2m': ['recipe']
    }

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)
    filter_horizontal = ()
    inlines = [CollectionRecipeInline,]
    #raw_id_fields = ('recipes',)
    #related_lookup_fields = {
    #    'm2m': ['recipes']
    #}
    
admin.site.register(Collection, CollectionAdmin)