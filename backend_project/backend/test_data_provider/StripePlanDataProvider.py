from domain.chefs.plan.Plan import Plan
from domain.stripe.StripePlan import StripePlan

class StripePlanDataProvider:

    def __init__(self, plan=Plan(type='pro', interval='monthly', amount_per_month=5)):
        self.stripe_plan = StripePlan(plan)

    @staticmethod
    def get(plan=Plan(type='pro', interval='monthly', amount_per_month=5)):
        return StripePlanDataProvider(plan)

    def build(self):
        return self.stripe_plan

    def withId(self, id):
        self.stripe_plan.id = id
        return self

    @staticmethod
    def getDefault(plan=Plan(type='pro', interval='monthly', amount_per_month=5)):
        p = StripePlanDataProvider(plan)
        return p.build()
