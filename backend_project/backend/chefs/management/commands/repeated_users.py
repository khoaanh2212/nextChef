from django.core.management.base import BaseCommand
from chefs.models import Chefs
from recipe.models import Recipes
from django.db.models import Count


class Command(BaseCommand):

    def handle(self, *args, **options):
        duplicated_chefs = Chefs.objects.values('email').annotate(num_email=Count('email')).filter(num_email__gt=1)
        for chef in duplicated_chefs:
            repeated_chefs = Chefs.objects.filter(email=chef['email'])
            #if repeated_chefs.count() > 1: #hi ha chefs amb diferent id i mateix mail
            repe = False
            num_id = -1
            numrepe = repeated_chefs.count()
            tmp_chef = None

            for one in repeated_chefs: #per cada chef repetit
                if one.recipes.count() > 0: #si te receptes
                    if not repe:
                        repe = True #a True si en alguna compte te receptes
                        num_id = one.id
                        tmp_chef = one
                    else:
                        self.stdout.write('ERROR per a CHEF: "%s"' % one.email)

                        if one.cache_recipes > tmp_chef.cache_recipes:
                            for recepta in tmp_chef.recipes.all():
                                recepta.chef_id = one.id
                                recepta.save()
                            tmp_chef.delete()
                        else:
                            for recepta in one.recipes.all():
                                recepta.chef_id = tmp_chef.id
                                recepta.save()
                            one.delete()

                        numrepe -= 1
                elif one.recipes.count() == 0 and numrepe > 1:
                    self.stdout.write('Deleting user %s-%s' % (one.id, one.email))
                    instance = Chefs.objects.get(id=one.id)
                    instance.delete()

                    numrepe -= 1
