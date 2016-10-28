import unittest
from mock import Mock, MagicMock

from domain.chefs.stripe_payment.StripePaymentService import StripePaymentService

class StripePaymentServiceTest(unittest.TestCase):
    '''
        Stripe Payment Service Test
    '''

    def setUp(self):
        self.repositoryStub = Mock()
        self.modelStub = Mock()
        self.sut = StripePaymentService.new(
            repository=self.repositoryStub,
            model=self.modelStub
        )

    def test_create_should_call_to_repository_with_model_object(self):
        self.repositoryStub.save.return_value = 'object'
        actual = self.sut.create('')
        self.assertEqual(actual, 'object')

    def test_getByPlanAndCustomer_should_return_a_StripePayment_object(self):
        self.repositoryStub.findByPlanAndCustomer.return_value = 'object'
        actual = self.sut.getByPlanAndCustomer('plan-id', 'customer-id')
        self.repositoryStub.findByPlanAndCustomer.assert_called_with('plan-id', 'customer-id')
        self.assertEqual(actual, 'object')
