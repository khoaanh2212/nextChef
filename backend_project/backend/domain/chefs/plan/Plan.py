from django.db import models


class Plan(models.Model):

    PLAN_CHOICES = (
        ("pro", "Pro"),
        ("business", "Business")
    )

    INTERVAL_CHOICES = (
        ("monthly", "Monthly"),
        ("annually", "Annually")
    )

    type = models.CharField(choices=PLAN_CHOICES, default='pro', max_length=255)
    interval = models.CharField(choices=INTERVAL_CHOICES, default='monthly', max_length=255)
    amount_per_month = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    amount_per_year = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    class Meta:
        db_table = 'plan'

    @classmethod
    def create(cls, type, interval, amount_per_month):
        amount_per_year = amount_per_month * 12
        plan = cls(
            type=type,
            interval=interval,
            amount_per_month=amount_per_month,
            amount_per_year=amount_per_year)
        return plan
