from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from chefs.models import Chefs
from recipe.models import Recipes
from django.db.models import Count
from django.db.models import Q
from django.core.urlresolvers import reverse


def list_users(self=None):
    # chefs = Chefs.objects.filter(~Q(language='es')&~Q(language='ca'))
    chefs = Chefs.objects.filter(Q(language='es') | Q(language='ca'))
    errors_counter = 0
    for chef in chefs:
        # if 1 < chef.recipes.filter(draft=0).count() < 4:
        if chef.recipes.filter(draft=0).count() < 2:
            try:
                name = chef.name
                email = chef.email
                '''
                header_image = chef.cover_thumb('email_header')
                chef_string = '"' + name + '","' + email + '","' + header_image + '"'
                recipes = chef.recipes.filter(draft=0).order_by('-final_score')[:2]
                for recipe in recipes:
                    chef_string += ',"' + recipe.name.replace('"', '') + '","' + recipe.thumb('email_cover') + '"'
                url = 'http://nextchef.co' + reverse('library', kwargs={'slug': chef.slug, 'id': chef.id})
                chef_string += ',"' + url + '"\n'
                '''
                chef_string = '"' + name + '","' + email + '"\n'
                if self:
                    self.stdout.write("%s" % chef_string)
                else:
                    print(chef_string)
            except Exception, e:
                errors_counter += 1
    if self:
        self.stdout.write("errors: %s" % errors_counter)
    else:
        print(errors_counter)


def list_active_users_and_pdf(self):
    link = 'http://nextchef.co'
    chefs = Chefs.objects.filter(recipes__draft=0).annotate(num_recipes=Count('recipes')).filter(num_recipes__gte=19)
    errors_counter = 0
    for chef in chefs:
        try:
            name = chef.name
            surname = chef.surname
            email = chef.email
            language = chef.language
            last_signin_date = str(chef.last_signin_date)
            best_recipe = chef.best_recipe
            if best_recipe:
                url = reverse('recipe_download_pdf', kwargs={'slug': best_recipe.slug, 'id': best_recipe.id})
                url = link + url
                chef_string = name + ', '+surname + ', ' + email + ', ' + language + ', ' +last_signin_date + ', ' + url
                print chef_string
            else:
                raise Exception
        except Exception:
            errors_counter += 1
    print "Errors: " + str(errors_counter)


class Command(BaseCommand):
    def handle(self, *args, **options):
        list_active_users_and_pdf(self)
