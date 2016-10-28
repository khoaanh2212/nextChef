from chefs.models import Chefs
from domain.InvalidArgumentException import InvalidDomainArgumentException
from .StripePlan import StripePlan

class StripeCustomer:
    def __init__(self, chef, token, stripePlan, id=''):
        if not isinstance(chef, Chefs):
            raise InvalidDomainArgumentException(chef)

        if not isinstance(stripePlan, StripePlan):
            raise InvalidDomainArgumentException(stripePlan)

        self.source = token
        self.plan = stripePlan.id
        self.email = chef.email
        self.id = id

    @staticmethod
    def new(chef, token, stripePlan):
        return StripeCustomer(chef, token, stripePlan)
