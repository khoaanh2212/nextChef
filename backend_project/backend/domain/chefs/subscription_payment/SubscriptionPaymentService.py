from .SubscriptionPayment import SubscriptionPayment
from infrastructure.chefs.subscription_payment.SubscriptionPaymentRepository import SubscriptionPaymentRepository


class SubscriptionPaymentService:

    '''Subscription Payment Service'''

    def __init__(self, repository, model):
        self.repository = repository
        self.model = model

    def create(self, subscription_id, payment_id):
        return self.repository.save(self.model.create(subscription_id, payment_id))

    def getByPaymentId(self, payment_id):
        return self.repository.findByPaymentId(payment_id)

    @staticmethod
    def new(repository=SubscriptionPaymentRepository.new(), model=SubscriptionPayment):
        return SubscriptionPaymentService(repository, model)
