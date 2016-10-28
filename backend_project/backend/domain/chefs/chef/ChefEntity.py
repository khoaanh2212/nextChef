from chefs.models import Chefs
from domain.InvalidArgumentException import InvalidDomainArgumentException

class ChefEntity:
    def __init__(self, model = Chefs):
        self.model = model

    def updateMembership(self, chef, membership):
        if not membership in [
            Chefs.MEMBERSHIP_DEFAULT,
            Chefs.MEMBERSHIP_PRO,
            Chefs.MEMBERSHIP_BUSINESS,
            Chefs.MEMBERSHIP_ENTERPRISE
        ]:
            raise InvalidDomainArgumentException

        chef.membership = membership
        return chef
