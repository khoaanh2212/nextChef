from django.contrib.sitemaps import Sitemap
from recipe.models import Recipes
from chefs.models import Chefs


class RecipesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Recipes.objects.explore_recipes()

    def lastmod(self, obj):
        return obj.edit_date
    
    def location(self, obj):
        return obj.full_url


class ChefsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Chefs.objects.chefs_pros()

    def lastmod(self, obj):
        return obj.edit_date

    def location(self, obj):
        return obj.site_url


class FoodiesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Chefs.objects.chefs_foodies()

    def lastmod(self, obj):
        return obj.edit_date

    def location(self, obj):
        return obj.site_url

sitemaps = {
    'recipes': RecipesSitemap,
    'chefs': ChefsSitemap,
    'foodies': FoodiesSitemap
}