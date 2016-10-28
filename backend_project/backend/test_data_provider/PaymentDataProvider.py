from domain.chefs.stripe_payment.StripePayment import StripePayment

class StripePaymentDataProvider:
    def __init__(self, payment=StripePayment(
        plan_id='1',
        customer_id='1',
        last4='1234',
        exp_month='12',
        exp_year='2018'
    )):
        self.payment = payment

    def build(self):
        return self.payment

    @staticmethod
    def get(payment=StripePayment(
        plan_id='1',
        customer_id='1',
        last4='1234',
        exp_month='12',
        exp_year='2018'
    )):
        return StripePaymentDataProvider(payment)

    @staticmethod
    def getDefault(payment=StripePayment(
        plan_id='1',
        customer_id='1',
        last4='1234',
        exp_month='12',
        exp_year='2018'
    )):
        data_provider = StripePaymentDataProvider(payment)
        return data_provider.build()
