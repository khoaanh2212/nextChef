# -*- coding: utf-8 -*-
import os, stripe
from south.v2 import DataMigration

from infrastructure.stripe.StripeGateway import StripeGateway
from domain.chefs.plan.Plan import Plan
from domain.stripe.StripePlan import StripePlan

class Migration(DataMigration):
    initial = True
    dependencies = [
        ('application', '0002_init_plans.py'),
    ]

    def forwards(self, orm):
        test_data = os.getenv('INIT_STRIPE_PLANS', 'false')
        if not test_data == 'true':
            return

        stripe_gateway = StripeGateway.new()
        plans = Plan.objects.all()
        for plan in plans:
            try:
                stripe_plan = StripePlan(plan)
                stripe_gateway.createPlan(stripe_plan)
            except(stripe.error.InvalidRequestError):
                print('Invalid stripe api request: ' + stripe.error.InvalidRequestError.message.__str__())
                pass

    def backwards(self, orm):
        pass

    complete_apps = ['application']
