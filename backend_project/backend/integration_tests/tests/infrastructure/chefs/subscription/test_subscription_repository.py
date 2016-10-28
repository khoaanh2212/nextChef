from chefs.models import Chefs
from domain.chefs.plan.Plan import Plan
from domain.chefs.subscription.Subscription import Subscription
from infrastructure.chefs.subscription.SubscriptionRepository import SubscriptionRepository
from integration_tests.integration_test_case import IntegrationTestCase


class SubscriptionRepositoryTest(IntegrationTestCase):
    '''
        SubscriptionRepository Test
    '''

    def setUp(self):
        super(SubscriptionRepositoryTest, self).setUp()
        self.sut = SubscriptionRepository()

    def test_save_should_save_and_return_plan_object(self):
        plan = self._mkPlan()
        chef = self._mkUser()
        subscription = self._mkSubscription(chef, plan)

        actual = self.sut.save(subscription)
        saved_subscription = Subscription.objects.get(chef=chef, plan=plan)

        self.assertIsNotNone(saved_subscription)
        self.assertEqual(actual, subscription)

    def _mkPlan(self):
        return Plan.objects.create(type='pro', interval='monthly', amount_per_month=1, amount_per_year=12)

    def _mkUser(self):
        return Chefs.objects.create_user('Test', 'Tests', 'test@example.com', 'secret')

    def _mkSubscription(self, chef, plan):
        return Subscription.create(chef=chef, plan=plan)
