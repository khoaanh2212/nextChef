from infrastructure.BaseRepository import BaseRepository
from domain.chefs.subscription_payment.SubscriptionPayment import SubscriptionPayment


class SubscriptionPaymentRepository(BaseRepository):
    def __init__(self, model=SubscriptionPayment):
        BaseRepository.__init__(self, model)

    def findByPaymentId(self, payment_id):
        return self.model.objects.get(stripe_payment_id=payment_id)

    @staticmethod
    def new(model=SubscriptionPayment):
        return SubscriptionPaymentRepository(model)
