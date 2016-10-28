from domain.BaseEntity import BaseEntity
from django.utils import timezone
from django.db import models

class StripePayment(models.Model):

    plan_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    last4 = models.IntegerField()
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()

    class Meta:
        db_table = 'stripe_payment'

    @classmethod
    def create(cls, payment_details):
        payment = cls(
            plan_id=payment_details['plan_id'],
            customer_id=payment_details['customer_id'],
            last4=payment_details['last4'],
            exp_month=payment_details['exp_month'],
            exp_year=payment_details['exp_year']
        )
        return payment
