from django.core.management.base import BaseCommand
from chefs.models import Chefs
from recipe.models import Recipes
from django.db.models import Count
from django.db.models import Q
from django.core.urlresolvers import reverse

def list_users(self=None):
    chefs = Chefs.objects.filter(~Q(language='es') &~Q(language='ca'))
    errors_counter = 0
    for chef in chefs:
        if chef.recipes.filter(draft=0).count() < 2:
            try:
                name = chef.name
                email = chef.email
                url = 'http://nextchef.co' + reverse('library', kwargs={'slug': chef.slug, 'id': chef.id})
                chef_string = name + ',' + email + ',' + url + '\n'
                
                if self:
                    self.stdout.write("%s" % chef_string)
                else:
                    print(chef_string);
            except:
                errors_counter += 1
    if self:
        self.stdout.write("errors: %s" % errors_counter)
    else:
        print(errors_counter);
                     
class Command(BaseCommand):

    def handle(self, *args, **options):
        list_users(self)
                
        
