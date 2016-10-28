# -*- coding: utf-8 -*-
from optparse import make_option
from datetime import datetime, time
from django.utils.timezone import utc
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Count

from chefs.models import ChefFollows
from recipe.models import Likes, Comments
from metrics.models import Metric
from metrics.geckoboard import GeckoBoard


class Command(BaseCommand):
    help = 'Count social actions (follow, love, save, comment.'
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

        # Follow actions
        cnt_follows = self._follows(pivot_date)
        GeckoBoard.push_weekly_metric(Metric.KPI_TOTAL_FOLLOWS)

        # Likes
        cnt_likes = self._likes(pivot_date)
        GeckoBoard.push_weekly_metric(Metric.KPI_TOTAL_LIKES)

        # Comments
        cnt_comments = self._comments(pivot_date)
        GeckoBoard.push_weekly_metric(Metric.KPI_TOTAL_COMMENTS)

        self.stdout.write("%s follow actions" % cnt_follows)
        self.stdout.write("%s likes actions" % cnt_likes)
        self.stdout.write("%s comments created" % cnt_comments)

    def _follows(self, pivot_date):
        pivot_date_min = datetime.combine(pivot_date, time(0, 0, 0, 0, tzinfo=utc))
        pivot_date_max = datetime.combine(pivot_date, time(23, 59, 59, 999999, tzinfo=utc))

        num_follows = ChefFollows.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max)).count()

        # Store data points
        Metric.insert_metric(Metric.KPI_TOTAL_FOLLOWS, pivot_date,  num_follows, segment=Metric.SEG_ALL)

        return num_follows

    def _likes(self, pivot_date):
        pivot_date_min = datetime.combine(pivot_date, time(0, 0, 0, 0, tzinfo=utc))
        pivot_date_max = datetime.combine(pivot_date, time(23, 59, 59, 999999, tzinfo=utc))

        num_likes = Likes.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max)).count()

        # Store data points
        Metric.insert_metric(Metric.KPI_TOTAL_LIKES, pivot_date,  num_likes, segment=Metric.SEG_ALL)

        return num_likes

    def _comments(self, pivot_date):
        pivot_date_min = datetime.combine(pivot_date, time(0, 0, 0, 0, tzinfo=utc))
        pivot_date_max = datetime.combine(pivot_date, time(23, 59, 59, 999999, tzinfo=utc))

        num_comments = Comments.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max)).count()

        # Store data points
        Metric.insert_metric(Metric.KPI_TOTAL_COMMENTS, pivot_date,  num_comments, segment=Metric.SEG_ALL)

        return num_comments

