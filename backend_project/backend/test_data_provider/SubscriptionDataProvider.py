from domain.chefs.subscription.Subscription import Subscription
from .PlanDataProvider import PlanDataProvider
from .ChefDataProvider import ChefDataProvider

class SubscriptionDataProvider:
    def __init__(self, subscription=Subscription(
        plan=PlanDataProvider.getDefault(),
        chef=ChefDataProvider.getDefault()
    )):
        self.subscription = subscription

    def build(self):
        return self.subscription

    def withPeriodStart(self, period_start):
        self.subscription.period_start = period_start
        return self

    def withPeriodEnd(self, period_end):
        self.subscription.period_end = period_end
        return self

    def withEndedAt(self, ended_at):
        self.subscription.ended_at = ended_at
        return self

    def withCanceledAt(self, canceled_at):
        self.subscription.canceled_at = canceled_at
        return self

    def withIsCanceledAtPeriodEnd(self, is_canceled_at_period_end):
        self.subscription.is_canceled_at_period_end = is_canceled_at_period_end
        return self

    def withStatus(self, status):
        self.subscription.status = status
        return self

    @staticmethod
    def get(subscription=Subscription(
        plan=PlanDataProvider.getDefault(),
        chef=ChefDataProvider.getDefault()
    )):
        return SubscriptionDataProvider(subscription)

    @staticmethod
    def getDefault(subscription=Subscription(
        plan=PlanDataProvider.getDefault(),
        chef=ChefDataProvider.getDefault()
    )):
        data_provider = SubscriptionDataProvider(subscription)
        return data_provider.build()
