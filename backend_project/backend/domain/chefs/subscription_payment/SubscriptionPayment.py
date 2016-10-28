from django.db import models


class SubscriptionPayment(models.Model):

    subscription_id = models.IntegerField()
    subscription_method = models.CharField(default="stripe", max_length=255)
    stripe_payment_id = models.IntegerField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'subscription_payment'

    @classmethod
    def create(cls, subscription_id, payment_id):
        return cls(
            subscription_id=subscription_id,
            stripe_payment_id=payment_id,
            is_active=True
        )
