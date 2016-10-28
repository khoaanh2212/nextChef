from infrastructure.chefs.stripe_payment.StripePaymentRepository import StripePaymentRepository
from .StripePayment import StripePayment

class StripePaymentService:

    '''StripePaymentService'''

    def __init__(self, repository, model):
        self.repository = repository
        self.model = model

    def create(self, payment_details):
        return self.repository.save(self.model.create(payment_details))

    def getByPlanAndCustomer(self, plan_id, customer_id):
        return self.repository.findByPlanAndCustomer(plan_id, customer_id)

    @staticmethod
    def new(repository=StripePaymentRepository.new(), model=StripePayment):
        return StripePaymentService(repository, model)
