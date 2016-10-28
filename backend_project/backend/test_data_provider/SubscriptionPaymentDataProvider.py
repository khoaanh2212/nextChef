from domain.chefs.subscription_payment.SubscriptionPayment import SubscriptionPayment
from .SubscriptionDataProvider import SubscriptionDataProvider
from .PaymentDataProvider import StripePaymentDataProvider

class SubscriptionPaymentDataProvider:
    def __init__(self, subscription_payment=SubscriptionPayment(
        subscription_id=1,
        stripe_payment_id=1,
        is_active=True
    )):
        self.subscription_payment = subscription_payment

    def build(self):
        return self.subscription_payment

    def withStripePaymentId(self, paymentId):
        self.subscription_payment.stripe_payment_id = paymentId
        return self

    @staticmethod
    def get(subscription_payment=SubscriptionPayment(
        subscription_id=1,
        stripe_payment_id=1,
        is_active=True
    )):
        return SubscriptionPaymentDataProvider(subscription_payment)

    @staticmethod
    def getDefault(subscription_payment=SubscriptionPayment(
        subscription_id=1,
        stripe_payment_id=1,
        is_active=True
    )):
        data_provider = SubscriptionPaymentDataProvider(subscription_payment)
        return data_provider.build()
