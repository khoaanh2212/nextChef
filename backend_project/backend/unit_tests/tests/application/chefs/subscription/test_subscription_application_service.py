import unittest
from mock import Mock, MagicMock
from application.chefs.subscription.SubscriptionApplicationService import SubscriptionApplicationService
from test_data_provider.SubscriptionDataProvider import SubscriptionDataProvider
from test_data_provider.StripePlanDataProvider import StripePlanDataProvider
from test_data_provider.StripeCustomerDataProvider import StripeCustomerDataProvider
from test_data_provider.PlanDataProvider import PlanDataProvider
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.SubscriptionPaymentDataProvider import SubscriptionPaymentDataProvider
from domain.stripe.StripeCustomer import StripeCustomer
from chefs.models import Chefs
from domain.stripe.StripePlan import StripePlan
from domain.chefs.plan.Plan import Plan
from domain.chefs.subscription.Subscription import Subscription



class SubscriptionApplicationService_startSubscriptionTest(unittest.TestCase):
    '''
        SubscriptionApplicationService Test
    '''

    PLAN = Plan()
    CHEF = Chefs()
    STRIPE_CUSTOMER = StripeCustomer.new(CHEF, 'token', StripePlan(PLAN))

    def setUp(self):
        self.subscriptionServiceStub = Mock()
        self.planServiceStub = Mock()
        self.paymentServiceStub = Mock()
        self.subscriptionPaymentServiceStub = Mock()
        self.stripeGatewayStub = Mock()
        self.chefServiceStub = Mock()
        self.sut = SubscriptionApplicationService.new(
            subscription_service=self.subscriptionServiceStub,
            plan_service=self.planServiceStub,
            payment_service=self.paymentServiceStub,
            subscription_payment_service=self.subscriptionPaymentServiceStub,
            stripe_gateway=self.stripeGatewayStub,
            chef_service=self.chefServiceStub
        )

    def test_startSubscription_returnsValidSubscription(self):
        self.subscriptionServiceStub.create.return_value = self._mkSubscription()
        self.planServiceStub.get.return_value = Plan()
        self.paymentServiceStub.create.return_value = self._mkPayment()
        self.stripeGatewayStub.createSubscription.return_value = self.STRIPE_CUSTOMER
        self.chefServiceStub.upgradeMembership.return_value = self.CHEF

        actual = self.sut.startSubscription(self.CHEF, 'plan_id', 'token', 'card_last4', 'card_expMonth', 'card_expYear')
        self.assertEquals(actual, self.CHEF)

    def test_updateSubscription_returnsUpdatedSubscription(self):
        self.subscriptionServiceStub.update.return_value = self._mkSubscription()
        self.paymentServiceStub.getByPlanAndCustomer.return_value = self._mkPayment()
        self.subscriptionPaymentServiceStub.getByPaymentId.return_value = SubscriptionPaymentDataProvider.getDefault()
        self.sut._updateMembership = MagicMock(name='updateMembership')

        self.sut.updateSubscription(self._mkSubscriptionDetails())
        self.sut._updateMembership.assert_called_with(self._mkSubscription())

    def test__updateMembership_should_cancel_membership_if_subscription_canceled(self):
        subscription = SubscriptionDataProvider.get().withStatus(Subscription.STATUS_CANCELED).build()
        self.sut._updateMembership(subscription)
        self.chefServiceStub.cancelMembership.assert_called_with(subscription.chef)

    def test__updateMembership_should_not_cancel_membership_if_subscription_not_canceled(self):
        for status in [Subscription.STATUS_STARTED, Subscription.STATUS_HOLDING]:
            subscription = SubscriptionDataProvider.get().withStatus(status).build()
            self.sut._updateMembership(subscription)
            self.assertFalse(self.chefServiceStub.cancelMembership.called)

    def _mkSubscription(self):
        subscription = SubscriptionDataProvider.getDefault()
        subscription.pk = 1
        return subscription

    def _mkPayment(self):
        payment = StripePlanDataProvider.getDefault()
        payment.pk = 1
        return payment

    def _mkSubscriptionDetails(self):
        return dict(
            customer = 'cus_1233',
	        plan = 'plan_1234',
	        ended_at = '1234567',
	        current_period_end = '1234567',
	        current_period_start = '1234567',
            canceled_at = '1234567',
            cancel_at_period_end = False
        )
