from domain.stripe.StripeCustomer import StripeCustomer
from .ChefDataProvider import ChefDataProvider
from .StripePlanDataProvider import StripePlanDataProvider

class StripeCustomerDataProvider:

    def __init__(
            self,
            chef=ChefDataProvider.getDefault(),
            token='token',
            stripePlan=StripePlanDataProvider.getDefault()
    ):
        self.chef = chef
        self.token = token
        self.stripePlan = stripePlan
        self.id = 1

    @staticmethod
    def get():
        return StripeCustomerDataProvider()

    def build(self):
        stripe_customer = StripeCustomer(self.chef, self.token, self.stripePlan, self.id)
        return stripe_customer

    def withId(self, id):
        self.id = id
        return self

    def withEmail(self, email):
        self.chef.email = email
        return self

    @staticmethod
    def getDefault():
        p = StripeCustomerDataProvider()
        return p.build()
