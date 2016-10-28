from infrastructure.BaseRepository import BaseRepository
from domain.chefs.stripe_payment.StripePayment import StripePayment

class StripeException(Exception):
    pass

class StripePaymentRepository(BaseRepository):
    def __init__(self, model=StripePayment):
        BaseRepository.__init__(self, model)

    def findByPlanAndCustomer(self, plan_id, customer_id):
        try:
            return StripePayment.objects.get(plan_id=plan_id, customer_id=customer_id)
        except Exception, e:
            raise StripeException(e)

    @staticmethod
    def new(model=StripePayment):
        return StripePaymentRepository(model)
