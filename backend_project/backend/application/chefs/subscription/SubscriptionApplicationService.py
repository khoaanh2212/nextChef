from domain.chefs.subscription.SubscriptionService import SubscriptionService
from domain.chefs.plan.PlanService import PlanService
from infrastructure.stripe.StripeGateway import StripeGateway
from domain.stripe.StripeCustomer import StripeCustomer
from domain.stripe.StripePlan import StripePlan
from domain.chefs.stripe_payment.StripePaymentService import StripePaymentService
from domain.chefs.subscription_payment.SubscriptionPaymentService import SubscriptionPaymentService
from domain.chefs.chef.ChefService import ChefService
from domain.chefs.subscription.Subscription import Subscription
import logging


class SubscriptionApplicationService:
    def __init__(
            self,
            subscription_service,
            plan_service,
            stripe_gateway,
            payment_service,
            subscription_payment_service,
            chef_service,
            logger
    ):
        self.subscription_service = subscription_service
        self.plan_service = plan_service
        self.stripe_gateway = stripe_gateway
        self.payment_service = payment_service
        self.subscription_payment_service = subscription_payment_service
        self.chef_service = chef_service
        self.logger = logger

    def startSubscription(self, chef, plan_id, token, card_last4, card_expMonth, card_expYear):
        plan = self.plan_service.get(plan_id)
        subscription = self.subscription_service.create(chef, plan)
        subscription_details = self._createStripeSubscription(chef, token, plan, card_last4, card_expMonth, card_expYear)
        payment = self.payment_service.create(subscription_details)
        self.subscription_payment_service.create(subscription.pk, payment.pk)
        return self.chef_service.upgradeMembership(chef.id, plan.type)

    def updateSubscription(self, subscription_details):
        self.logger.info('Webhook sent: Plan: %s - Customer: %s', subscription_details['plan'], subscription_details['customer'])
        self.logger.debug(subscription_details)
        payment = self.payment_service.getByPlanAndCustomer(subscription_details['plan'], subscription_details['customer'])
        subscription_payment = self.subscription_payment_service.getByPaymentId(payment.id)
        subscription = self.subscription_service.update(subscription_payment.subscription_id, subscription_details)
        self._updateMembership(subscription)

    def _updateMembership(self, subscription):
        if subscription.status == Subscription.STATUS_CANCELED:
            self.chef_service.cancelMembership(subscription.chef)
            self.logger.info('Subscription canceled: %s', subscription.id)
            self.logger.debug(subscription)

    def _createStripeSubscription(self, chef, token, plan, card_last4, card_expMonth, card_expYear):
        stripe_plan = StripePlan(plan)
        customer = StripeCustomer(chef, token, stripe_plan)
        stripe_customer_id = self.stripe_gateway.createSubscription(customer)
        return dict(
            customer_id = stripe_customer_id,
            plan_id = stripe_plan.id,
            last4 = card_last4,
            exp_month = card_expMonth,
            exp_year = card_expYear
        )

    @staticmethod
    def new(
            subscription_service=SubscriptionService.new(),
            plan_service=PlanService.new(),
            stripe_gateway=StripeGateway.new(),
            payment_service=StripePaymentService.new(),
            subscription_payment_service=SubscriptionPaymentService.new(),
            chef_service=ChefService.new(),
            logger = logging.getLogger('Subscription')
    ):
        return SubscriptionApplicationService(subscription_service, plan_service, stripe_gateway, payment_service, subscription_payment_service, chef_service, logger)
