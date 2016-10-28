from django.db import models
from django.utils import timezone
import datetime

from chefs.models import Chefs
from domain.chefs.plan.Plan import Plan

class Subscription(models.Model):

    STATUS_STARTED = 'started'
    STATUS_CANCELED = 'canceled'
    STATUS_HOLDING = 'holding'

    STATUSES = (
        (STATUS_STARTED, 'Started'),
        (STATUS_CANCELED, 'Canceled'),
        (STATUS_HOLDING, 'Holding')
    )

    chef = models.ForeignKey(Chefs, related_name="+")
    plan = models.ForeignKey(Plan, related_name="+")
    started_at = models.DateTimeField(default=datetime.datetime.now())
    period_start = models.DateTimeField(default=datetime.datetime.now())
    period_end = models.DateTimeField(blank=True, null=True, default=None)
    ended_at = models.DateTimeField(blank=True, null=True, default=None)
    canceled_at = models.DateTimeField(blank=True, null=True, default=None)
    status = models.CharField(choices=STATUSES, default='started', max_length=255)
    is_canceled_at_period_end = models.BooleanField(default=False)

    class Meta:
        db_table = 'subscription'

    @classmethod
    def create(cls, chef, plan):
        now = timezone.now()
        return cls(chef=chef, plan=plan, started_at=now, period_start=now)

    @classmethod
    def update(cls, subscription, subscription_details):
        subscription.period_start = datetime.datetime.fromtimestamp(int(subscription_details['period_start']))
        subscription.period_end = datetime.datetime.fromtimestamp(int(subscription_details['period_end']))
        subscription.ended_at = datetime.datetime.fromtimestamp(int(subscription_details['ended_at']))
        subscription.canceled_at = datetime.datetime.fromtimestamp(int(subscription_details['canceled_at']))
        subscription.is_canceled_at_period_end = subscription_details['is_canceled_at_period_end']

        if subscription.ended_at is not None or subscription.canceled_at is not None:
            subscription.status = cls.STATUS_CANCELED

        return subscription
