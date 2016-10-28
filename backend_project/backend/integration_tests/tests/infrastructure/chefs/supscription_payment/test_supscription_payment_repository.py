from domain.chefs.subscription_payment.SubscriptionPayment import SubscriptionPayment
from infrastructure.chefs.subscription_payment.SubscriptionPaymentRepository import SubscriptionPaymentRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.SubscriptionPaymentDataProvider import SubscriptionPaymentDataProvider


class SubscriptionPaymentRepositoryTest(IntegrationTestCase):
    '''
        SubscriptionRepository Test
    '''
    def setUp(self):
        super(SubscriptionPaymentRepositoryTest, self).setUp()
        self.sut = SubscriptionPaymentRepository()

    def test_insert_should_save_and_return_payment_object(self):
        subscription_payment = SubscriptionPaymentDataProvider.getDefault()

        actual = self.sut.save(subscription_payment)
        saved = SubscriptionPayment.objects.get(id=actual.pk)

        self.assertIsNotNone(saved)
        self.assertEqual(actual, saved)

    def test_findById_should_return_payment_object(self):
        subscription_payment = SubscriptionPaymentDataProvider.getDefault()
        saved = self.sut.save(subscription_payment)

        actual = self.sut.findById(saved.id)

        self.assertEqual(actual, subscription_payment)

    def test_findByPaymentId_should_return_payment_object(self):
        payment_id = 123
        subscription_payment = SubscriptionPaymentDataProvider.get().withStripePaymentId(payment_id).build()
        self.sut.save(subscription_payment)

        actual = self.sut.findByPaymentId(payment_id)

        self.assertEqual(actual, subscription_payment)
