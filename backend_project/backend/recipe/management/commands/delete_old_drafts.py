# -*- coding: utf-8 -*-
from datetime import timedelta
from optparse import make_option

from django.utils.timezone import now
from django.db.models import Count
from django.core.management.base import BaseCommand

from recipe.models import Recipes


class Command(BaseCommand):
    help = 'Delete recipes in draft mode older than 3 months'
    option_list = BaseCommand.option_list + (
        make_option('--days',
                    action='store',
                    help='Days old'),
        make_option('--no-dry-run',
                    action='store_false',
                    dest='dry-run',
                    default=True,
                    help='Enable real mode and update database'),
    )
    update_data = False

    def handle(self, *args, **options):
        if not options['days']:
            self.stderr.write("You must specify either --days=30 or --days=90")
            return
        else:
            days = int(options['days'])

        if options['dry-run']:
            self.update_data = False
        else:
            self.update_data = True

        after = now() - timedelta(days)

        self.stdout.write("Borrar recetas en borrador creadas antes de: %s" % after)

        recipes = Recipes.objects.filter(draft=True, creation_date__lte=after)\
                         .annotate(num_photos=Count('photos'))\
                         .filter(num_photos=0)

        k = 0
        d = 0
        for recipe in recipes:
            k += 1
            if self.update_data:
                recipe.delete()
                d += 1

        self.stdout.write("Recipes processed\t%s" % k)
        self.stdout.write("Recipes deleted\t\t%s" % d)
