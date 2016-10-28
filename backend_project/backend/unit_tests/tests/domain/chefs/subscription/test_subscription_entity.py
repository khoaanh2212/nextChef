import unittest, datetime
from domain.chefs.subscription.Subscription import Subscription
from test_data_provider.SubscriptionDataProvider import SubscriptionDataProvider

class SubscriptionTest(unittest.TestCase):

    def setUp(self):
        self.sut = Subscription

    def test_update_should_return_updated_object(self):
        subscription = SubscriptionDataProvider.get()\
            .withPeriodStart(datetime.datetime(2015, 1, 1))\
            .withPeriodEnd(datetime.datetime(2015, 1, 1))\
            .withCanceledAt(datetime.datetime(2015, 1, 1))\
            .withEndedAt(datetime.datetime(2015, 1, 1))\
            .withIsCanceledAtPeriodEnd(False)\
            .build()

        update_subscription_details = dict(
            period_start = '1451606400',
            period_end = '1451606400',
            canceled_at = '1451606400',
            ended_at = '1451606400',
            is_canceled_at_period_end = True
        )

        expected = SubscriptionDataProvider.get()\
            .withPeriodStart(datetime.datetime(2016, 1, 1))\
            .withPeriodEnd(datetime.datetime(2016, 1, 1))\
            .withCanceledAt(datetime.datetime(2016, 1, 1))\
            .withEndedAt(datetime.datetime(2016, 1, 1))\
            .withIsCanceledAtPeriodEnd(True)\
            .build()

        actual = self.sut.update(subscription, update_subscription_details)

        self.assertEqual(actual, expected)


    def _create(self, subscription):
        subscription.save()
        return subscription
