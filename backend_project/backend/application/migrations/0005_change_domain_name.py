import os
from south.v2 import DataMigration
from django.contrib.sites.models import Site

class Migration(DataMigration):
    def forwards(self,orm):
        try:
            site = Site.objects.get(pk=1)
            site.domain = 'bii.nextchef.co'
            site.name = 'NextChef'
            site.save()
        except:
            raise RuntimeError('can not change domain name')

    def backwards(self,orm):
        raise RuntimeError('can not go backwards')