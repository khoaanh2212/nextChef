from south.v2 import DataMigration
from domain.chefs.plan.Plan import Plan
from django.db.models import Q
import os

class Migration(DataMigration):
    def forwards(self, orm):
        # update price for pro annually user
        pro_annually = self.getPlan('pro','annually')
        if pro_annually:
            pro_annually.amount_per_month = 19.90
            pro_annually.amount_per_year = 19.90 * 11
            pro_annually.save()

        # update price for pro monthly user
        pro_monthly = self.getPlan('pro','monthly')
        if pro_monthly:
            pro_monthly.amount_per_month = 19.90
            pro_monthly.amount_per_year = 19.90 * 11
            pro_monthly.save()

        # update price for business annually
        business_annually = self.getPlan('business','annually')
        if business_annually:
            business_annually.amount_per_month = 59
            business_annually.amount_per_year = 59 * 11
            business_annually.save()

        # update price for business annually
        business_monthly = self.getPlan('business','monthly')
        if business_monthly:
            business_monthly.amount_per_month = 59
            business_monthly.amount_per_year = 59 * 11
            business_monthly.save()

    def backwards(self, orm):
        raise RuntimeError("Can't run backwards")

    def getPlan(self, type, interval):
        try:
            return Plan.objects.get(type=type, interval=interval)
        except:
            return False