from domain.chefs.plan.Plan import Plan
from domain.InvalidArgumentException import InvalidDomainArgumentException

class StripePlan:
    def __init__(self, plan, currency='usd'):
        if not isinstance(plan, Plan):
            raise InvalidDomainArgumentException

        self.id = self._getId(plan)
        self.name = plan.type
        self.interval = self._getIntervalForGateway(plan)
        self.amount = self._getAmountInCent(plan)
        self.currency = currency

    def _getId(self, plan):
        return plan.type.replace(' ', '_') + '__' + plan.interval

    def _getAmountInCent(self, plan):
        amount = plan.amount_per_month if plan.interval == 'monthly' else plan.amount_per_year
        return int(amount * 100)

    def _getIntervalForGateway(self, plan):
        return 'month' if plan.interval == 'monthly' else 'year'

    @staticmethod
    def new(plan, currency='usd'):
        return StripePlan(plan, currency)
