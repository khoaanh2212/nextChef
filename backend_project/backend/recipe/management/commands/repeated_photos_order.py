from django.core.management.base import BaseCommand
from chefs.models import Chefs
from recipe.models import Recipes, Photos
from django.db.models import Count, Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = '''select distinct(p.recipe_id) as id from photos p where p.photo_order in (select pp.photo_order from photos pp where pp.photo_order = p.photo_order and p.id != pp.id) group by p.recipe_id, p.photo_order having count(*) > 1 order by p.photo_order;'''
        for recipe in Photos.objects.raw(query):
            first = False
            count = 1
            for step in Photos.objects.all().filter(recipe=recipe):
                if step.photo_order is not None and not first:
                    first = True
                if first:
                    print "First: %s order: %s" % (step.id, count)
                    step.photo_order = count
                    count += 1
                    step.save()
            for step2 in Photos.objects.all().filter(recipe=recipe).exclude(~Q(photo_order=None)):
                if step2.photo_order is None:
                    print "None found: %s new_order: %s" % (step2.id, count)
                    step2.photo_order = count
                    count += 1
                    step2.save()
                else:
                    break