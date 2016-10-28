import stripe as Stripe
from django.conf import settings
import logging

class StripeGateway:

    def __init__(self, stripe, logger):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_KEY_SECRET
        self.logger = logger

    def createPlan(self, plan):
        return self.stripe.Plan.create(
            amount = plan.amount,
            interval = plan.interval,
            name = plan.name,
            currency = plan.currency,
            id = plan.id
        )

    def deletePlan(self, plan_id):
        plan = self.stripe.Plan.retrieve(plan_id)
        return plan.delete()

    def createSubscription(self, customer):

        self.logger.info('Customer %s created on stripe', customer.email)
        self.logger.debug(customer)

        result = self.stripe.Customer.create(
            source = customer.source,
            plan = customer.plan,
            email = customer.email
        )

        self.logger.info('Response from stripe %s', result.__str__())
        return result['id']

    @staticmethod
    def new(stripe=Stripe, logger=logging.getLogger('Stripe')):
        return StripeGateway(stripe, logger)
