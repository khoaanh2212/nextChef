import unittest
from mock import Mock

from domain.chefs.subscription_payment.SubscriptionPaymentService import SubscriptionPaymentService

class SubscriptionPaymentServiceTest(unittest.TestCase):
    '''
        Subscription Payment Service Test
    '''

    def setUp(self):
        self.repositoryStub = Mock()
        self.modelStub = Mock()
        self.sut = SubscriptionPaymentService.new(
            repository=self.repositoryStub,
            model=self.modelStub
        )

    def test_create_should_call_to_repository_with_model_object(self):
        self.repositoryStub.save.return_value = 'object'
        actual = self.sut.create('1', '1')
        self.assertEqual(actual, 'object')

    def test_getByPaymentId_should_return_a_SubscriptionPayment_object(self):
        self.repositoryStub.findByPaymentId.return_value = 'object'
        actual = self.sut.getByPaymentId('payment-id')
        self.repositoryStub.findByPaymentId.assert_called_with('payment-id')
        self.assertEqual(actual, 'object')
