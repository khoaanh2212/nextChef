# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Count

from recipe.models import RecipesManager
from recipe.searchers import RecipeMapping
from backend.esutils import index_objects


class Command(BaseCommand):
    help = 'Reindex visible recipes with more than three photos.'

    def handle(self, *args, **options):
        es = RecipeMapping.get_es()

        recipes = RecipeMapping.get_model().objects.filter(draft=False, private=False)\
            .annotate(photos_count=Count('photos'))\
            .filter(photos_count__gt=3)

        all_recipes_ids = list(recipes.values_list('pk', flat=True))

        index_objects(RecipeMapping, all_recipes_ids)

        self.stdout.write("Index for recipes created.")
