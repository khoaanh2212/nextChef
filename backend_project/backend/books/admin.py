from django.contrib import admin

from .models import Book, BookHasRecipes, ChefsHasBooks
from django.db.models import get_model

'''
class BooksAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ('name', 'chef', 'nb_shares', 'nb_comments', 'nb_added', 'creation_date', 'edit_date', 'added',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('-creation_date',)
    filter_horizontal = ()


'''

class ChefsHasBooksInline(admin.TabularInline):
    model = ChefsHasBooks
    fields = ('chef',)
    extra = 0
    raw_id_fields = ('chef',)
    related_lookup_fields = {
        'm2m': ['chef']
    }

class BookHasRecipesInline(admin.TabularInline):
    model = BookHasRecipes
    fields = ('recipe',)
    extra = 0
    raw_id_fields = ('recipe',)
    related_lookup_fields = {
        'm2m': ['recipe']
    }

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'chef', 'nb_shares', 'nb_comments', 'nb_added', 'creation_date', 'edit_date', 'added',)
    search_fields = ('id', 'name',)
    #fields = ('name',)
    filter_horizontal = ()
    inlines = [BookHasRecipesInline, ChefsHasBooksInline]
    raw_id_fields = ('chef',)
    related_lookup_fields = {
        'm2m': ['recipes']
    }
    

admin.site.register(Book, BookAdmin)
