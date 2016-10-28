# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Count

from recipe.models import Recipes


class Command(BaseCommand):
    help = 'Build ingredients order'

    def handle(self, *args, **options):

        recipes = Recipes.objects.filter(ingredients_order='N;')

        k = 0
        for r in recipes:
            ingredients = r.ingredients.all()
            if ingredients:
                r.set_ingredients_order(ingredients)
                r.save()
                k += 1

        self.stdout.write("%s recipes updated" % k)
