# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from recipe.searchers import RecipeMapping
from ...models import Recipes


class Command(BaseCommand):
    help = 'Search recipes.'
    args = "<string to search>"
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        if not len(args):
            self.stderr.write("You must specify a string to search")
            return
        fields = []
        fields += ['recipe']
        fields += ['chef']
        fields += ['book']
        fields += ['ingredient']
        fields += ['tag']

        results = RecipeMapping.cookbooth_search(args[0], fields)
        for r in results:
            try:
                if r.es_meta.score >= 0.5:
                    recipe = r.get_object()
                    self.stdout.write("[%s] -  %s - score: (%s)" % (recipe.pk, recipe.name, r.es_meta.score))
            except Recipes.DoesNotExist:
                self.stdout.write("El documento: %s no existe en la bdd" % r)
