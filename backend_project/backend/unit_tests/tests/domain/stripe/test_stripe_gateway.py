import mock
from django.test import TestCase

from infrastructure.stripe.StripeGateway import StripeGateway
from test_data_provider.PlanDataProvider import PlanDataProvider
from test_data_provider.StripePlanDataProvider import StripePlanDataProvider
from test_data_provider.StripeCustomerDataProvider import StripeCustomerDataProvider


class StripeGatewayTest(TestCase):
    '''
        StripeGateway test
    '''

    def setUp(self):
        self.loggerStub = mock.Mock()
        self.stripeStub = mock.Mock()
        self.sut = StripeGateway.new(self.stripeStub, self.loggerStub)

        self.defaultPlan = PlanDataProvider.getDefault()
        self.stripePlan = StripePlanDataProvider.getDefault()
        self.stripeStub.Customer.create.return_value = dict(
            id = 1234
        )

    def test_createPlan_should_create_plan_in_stripe(self):
        self.sut.stripe.Plan.create.return_value = {}
        actual = self.sut.createPlan(self.stripePlan)
        self.assertEqual(actual, {})

    def test_deletePlan_should_delete_plan_from_stripe(self):
        plan = mock.Mock(name='plan')
        self.sut.stripe.Plan.retrieve = mock.MagicMock('retrieve').return_value = plan
        planObj = plan()
        planObj.delete.return_value = 'deleted'
        actual = self.sut.deletePlan('')
        self.assertTrue(planObj.delete.called)
        self.assertTrue(actual, 'deleted')

    def test_createSubscription_should_create_subscription(self):
        customer = StripeCustomerDataProvider.get().withEmail('a@m.c').build()
        actual = self.sut.createSubscription(customer)
        self.assertEqual(actual, 1234)

    def test_createSubscription_should_write_log(self):
        customer = StripeCustomerDataProvider.get().withEmail('a@m.c').build()
        self.sut.createSubscription(customer)
        self.assertTrue(self.loggerStub.info.called)
