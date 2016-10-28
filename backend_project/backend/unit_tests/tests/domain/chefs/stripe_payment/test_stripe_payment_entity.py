import unittest
from domain.chefs.stripe_payment.StripePayment import StripePayment

class StripePaymentEntityTest(unittest.TestCase):
    '''
        Stripe Payment Entity
    '''

    def setUp(self):
        self.sut = StripePayment

    def test_create_should_translate_payment_details_to_StripePayment_object(self):
        payment_details = self._mkPaymentDetails()
        actual = self.sut.create(payment_details)
        self.assertEqual(actual.plan_id, '1')
        self.assertEqual(actual.customer_id, '1')
        self.assertEqual(actual.last4, '1234')
        self.assertEqual(actual.exp_month, '12')
        self.assertEqual(actual.exp_year, '2018')

    def _mkPaymentDetails(self):
        return dict(
            plan_id = '1',
            customer_id = '1',
            last4 = '1234',
            exp_month = '12',
            exp_year = '2018'
        )