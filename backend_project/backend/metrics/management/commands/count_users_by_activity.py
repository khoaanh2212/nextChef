# -*- coding: utf-8 -*-
from optparse import make_option
from datetime import time
from django.utils.timezone import utc
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Count

from chefs.models import Chefs
from metrics.models import Metric


class Command(BaseCommand):
    help = 'Count users by activity.'
    option_list = BaseCommand.option_list + (
        make_option('--date',
                    action='store',
                    dest='custom_date',
                    default=None,
                    help='Get data based on this date'),
        make_option('--days',
                    action='store',
                    dest='days',
                    default=None,
                    help='Number of days to check'),
    )

    def handle(self, *args, **options):
        num_days = int(options.get('days', 7))

        if options['custom_date']:
            end_date = datetime.strptime(options['custom_date'], '%Y-%m-%d')
        else:
            end_date = now() - timedelta(days=1)

        begin_date = end_date - timedelta(days=num_days)

        begin_date_min = datetime.combine(begin_date, time(0, 0, 0, 0, tzinfo=utc))
        end_date_max = datetime.combine(end_date, time(23, 59, 59, 999999, tzinfo=utc))

        users = Chefs.objects.values('type')\
            .filter(last_signin_date__range=(begin_date_min, end_date_max))\
            .annotate(Count('type'))
#            .exclude(creation_date=F(last_signin_date))

        cnt_pro = 0
        cnt_foodie = 0
        for row in users:
            if row['type'] == Chefs.TYPE_PRO:
                cnt_pro += row['type__count']
            else:
                cnt_foodie += row['type__count']

        # Store data points
        if num_days == 7:
            metric_code = Metric.KPI_SUPERACTIVE_USERS
        elif num_days == 30:
            metric_code = Metric.KPI_ACTIVE_USERS
        elif num_days == 60:
            metric_code = Metric.KPI_SLEEPING_USERS
        else:
            metric_code = Metric.KPI_DEAD_USERS

        Metric.insert_metric(metric_code, end_date, cnt_foodie, segment=Metric.SEG_FOODIES)
        Metric.insert_metric(metric_code, end_date, cnt_pro, segment=Metric.SEG_CHEFS)
        Metric.insert_metric(metric_code, end_date, cnt_pro + cnt_foodie, segment=Metric.SEG_ALL)

        self.stdout.write("%s user(s) registered" % (cnt_pro + cnt_foodie))
