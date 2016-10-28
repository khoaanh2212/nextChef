from domain.chefs.stripe_payment.StripePayment import StripePayment
from infrastructure.chefs.stripe_payment.StripePaymentRepository import StripePaymentRepository
from integration_tests.integration_test_case import IntegrationTestCase


class StripePaymentRepositoryTest(IntegrationTestCase):
    '''
        SubscriptionRepository Test
    '''

    def setUp(self):
        super(StripePaymentRepositoryTest, self).setUp()
        self.sut = StripePaymentRepository()

    def test_insert_should_save_and_return_payment_object(self):
        payment = self._mkPayment()

        actual = self.sut.save(payment)
        saved = StripePayment.objects.get(id=actual.pk)

        self.assertIsNotNone(saved)
        self.assertEqual(saved, payment)

    def test_findByPlanAndCustomer_should_return_correct_payment_object(self):
        payment = self._mkPayment('10', '10')
        self.sut.save(payment)

        actual = self.sut.findByPlanAndCustomer('10', '10')
        self.assertEqual(actual, payment)

    def _mkPayment(self, plan_id='1', customer_id='1'):
        return StripePayment(
            plan_id=plan_id,
            customer_id=customer_id,
            last4='1234',
            exp_month='12',
            exp_year='2018'
        )
