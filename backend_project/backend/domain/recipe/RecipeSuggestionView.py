from django.db import models
from chefs.models import Chefs


class RecipeSuggestionView(models.Model):

    id = models.CharField(primary_key=True, max_length=255)
    book_id = models.IntegerField(blank=True)
    recipe_id = models.IntegerField(blank=True)
    book_type = models.CharField(max_length=255, blank=True)
    chef_id = models.TextField(blank=True)
    recipe_name = models.CharField(max_length=255, blank=True)
    collaborators = models.TextField(blank=True)
    recipe_is_draft = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'recipe_suggestion_view'

    def to_dto(self):

        try:
            if self.chef_id:
                id = self.chef_id.split(',')[0]
                chef = Chefs.objects.get(id=id)
                chef_name = chef.name + ' ' + chef.surname
            else:
                chef_name = ''
        except Chefs.DoesNotExist:
            print('Chef does not exist')
            chef_name = ''

        return {
            "id": self.recipe_id,
            "name": self.recipe_name,
            "chef": {
                "name": chef_name,
                "id": self.chef_id
            }
        }
