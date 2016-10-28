from django.db import models


class Edamam(models.Model):

    request = models.TextField(blank=True)
    response = models.TextField(blank=True)

    class Meta:
        db_table = 'edamam'

    @classmethod
    def create(cls, request, response):
        return cls(request=request, response=response)
