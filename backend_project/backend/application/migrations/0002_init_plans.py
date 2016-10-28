# -*- coding: utf-8 -*-
from south.v2 import DataMigration

from domain.chefs.plan.PlanService import PlanService


class Migration(DataMigration):
    initial = True

    def forwards(self, orm):
        service = PlanService()
        service.create('pro', 'annually', 4.90)
        service.create('pro', 'monthly', 5.90)
        service.create('business', 'annually', 49)
        service.create('business', 'monthly', 59)

    def backwards(self, orm):
        pass

    complete_apps = ['application']
