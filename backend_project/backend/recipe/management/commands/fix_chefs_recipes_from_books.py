# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Count

from books.models import Book

from ...models import ChefsHasRecipes


class Command(BaseCommand):
    help = "Create relations between chefs and recipes from chefs' books copied"

    def handle(self, *args, **options):
        books = Book.objects.annotate(num_chefs=Count('chefs')).filter(num_chefs__gt=0)
        self.stdout.write("%d books" % books.count())
        for book in books:
            chefs = book.chefs.all()
            recipes = book.public_recipes(None)
            self.stdout.write("%s: %d chefs, %d recipes" % (book.name, chefs.count(), recipes.count()))
            for chef in chefs:
                chef_recipes = [i[0] for i in chef.recipes_added.all().values_list()]
                for recipe in recipes:
                    if recipe.chef == chef or recipe.pk in chef_recipes:
                        continue
                    ChefsHasRecipes.objects.create(chef=chef, recipe=recipe)
