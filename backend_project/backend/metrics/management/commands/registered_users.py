# -*- coding: utf-8 -*-
from optparse import make_option
from datetime import datetime, time
from django.utils.timezone import utc
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Count

from chefs.models import Chefs
from metrics.models import Metric
from metrics.geckoboard import GeckoBoard


class Command(BaseCommand):
    help = 'Count registered users.'
    option_list = BaseCommand.option_list + (
        make_option('--date',
                    action='store',
                    dest='custom_date',
                    default=None,
                    help='Get data based on this date'),
    )

    def handle(self, *args, **options):

        if options['custom_date']:
            pivot_date = datetime.strptime(options['custom_date'], '%Y-%m-%d')
        else:
            pivot_date = now() - timedelta(days=1)

        pivot_date_min = datetime.combine(pivot_date, time(0, 0, 0, 0, tzinfo=utc))
        pivot_date_max = datetime.combine(pivot_date, time(23, 59, 59, 999999, tzinfo=utc))

        registered_users = Chefs.objects.values('type')\
            .filter(creation_date__range=(pivot_date_min, pivot_date_max))\
            .annotate(Count('type'))

        cnt_pro = 0
        cnt_foodie = 0
        for row in registered_users:
            if row['type'] == Chefs.TYPE_PRO:
                cnt_pro += row['type__count']
            else:
                cnt_foodie += row['type__count']

        # Store data points
        Metric.insert_metric(Metric.KPI_REGISTERED_USERS, pivot_date, cnt_foodie, segment=Metric.SEG_FOODIES)
        Metric.insert_metric(Metric.KPI_REGISTERED_USERS, pivot_date, cnt_pro, segment=Metric.SEG_CHEFS)
        Metric.insert_metric(Metric.KPI_REGISTERED_USERS, pivot_date, cnt_pro + cnt_foodie, segment=Metric.SEG_ALL)

        # Count total foodies
        total_foodies = Chefs.objects.filter(is_active=True, active=True, type=Chefs.TYPE_FOODIE).count()
        Metric.insert_metric(Metric.KPI_TOTAL_USERS, pivot_date, total_foodies, segment=Metric.SEG_FOODIES)

        total_chefs = Chefs.objects.filter(is_active=True, active=True, type=Chefs.TYPE_PRO).count()
        Metric.insert_metric(Metric.KPI_TOTAL_USERS, pivot_date, total_chefs, segment=Metric.SEG_CHEFS)

        # Push to dashboard
        GeckoBoard.push_weekly_metric(Metric.KPI_REGISTERED_USERS)

        self.stdout.write("%s user(s) registered" % (cnt_pro + cnt_foodie))
        self.stdout.write("Total foodies %s registered" % total_foodies)
        self.stdout.write("Total chefs %s registered" % total_chefs)
