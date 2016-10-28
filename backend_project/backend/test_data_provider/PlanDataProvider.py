from domain.chefs.plan.Plan import Plan

class PlanDataProvider:

    def __init__(self):
        self.plan = Plan(type='pro', interval='monthly', amount_per_month=5)

    @staticmethod
    def get():
        return PlanDataProvider()

    def withType(self, type):
        self.plan.type = type
        return self

    def withInterval(self, interval):
        self.plan.interval = interval
        return self

    def withAmountPerMonth(self, amount):
        self.plan.amount_per_month = amount
        return self

    def withAmountPerYear(self, amount):
        self.plan.amount_per_year = amount
        return self

    def withId(self, id):
        self.plan.id = id
        return self

    def build(self):
        return self.plan

    @staticmethod
    def getDefault():
        plan = PlanDataProvider()
        return plan.build()
