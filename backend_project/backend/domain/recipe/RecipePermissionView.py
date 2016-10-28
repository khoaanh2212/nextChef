from django.db import models


class RecipePermissionView(models.Model):

    id = models.CharField(primary_key=True, max_length=255)
    recipe_chef_id = models.IntegerField(blank=True)
    book_chef_id = models.IntegerField(blank=True)
    collaborators = models.TextField(blank=True)
    state = models.CharField(blank=True, max_length=255)
    recipe_id = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'recipe_permission_view'

    def to_dto(self):
        return {}

