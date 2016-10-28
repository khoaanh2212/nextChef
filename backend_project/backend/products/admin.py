from django.contrib import admin

from products.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'shop_url')
    search_fields = ('name', 'shop_url', 'shop_title')
    filter_horizontal = ()
    raw_id_fields = ('recipe',)
    related_lookup_fields = {
        'recipes_m2m': ['recipe']
    }
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)