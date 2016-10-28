# -*- coding: utf-8 -*-
from optparse import make_option
from datetime import datetime, time
from django.utils.timezone import utc
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Count

from chefs.models import Chefs
from recipe.models import Recipes
from metrics.models import Metric
from metrics.geckoboard import GeckoBoard


class Command(BaseCommand):
    help = 'Count recipes created.'
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

        cnt_foodie = Recipes.objects.filter(draft=0,
                                            private=0,
                                            creation_date__range=(pivot_date_min, pivot_date_max),
                                            chef__type=Chefs.TYPE_FOODIE).count()

        cnt_pro = Recipes.objects.filter(draft=0,
                                         private=0,
                                         creation_date__range=(pivot_date_min, pivot_date_max),
                                         chef__type=Chefs.TYPE_PRO).count()

        # Store data points
        Metric.insert_metric(Metric.KPI_TOTAL_RECIPES, pivot_date, cnt_foodie, segment=Metric.SEG_FOODIES)
        Metric.insert_metric(Metric.KPI_TOTAL_RECIPES, pivot_date, cnt_pro, segment=Metric.SEG_CHEFS)

        # Count recipes with more than 3 photos
        cnt_foodie_plus_3 = Recipes.objects.filter(draft=0, private=0,
                                                   creation_date__range=(pivot_date_min, pivot_date_max),
                                                   chef__type=Chefs.TYPE_FOODIE)\
            .annotate(photos_count=Count('photos'))\
            .filter(photos_count__gt=3).count()

        cnt_pro_plus_3 = Recipes.objects.filter(draft=0, private=0,
                                                creation_date__range=(pivot_date_min, pivot_date_max),
                                                chef__type=Chefs.TYPE_PRO)\
            .annotate(photos_count=Count('photos'))\
            .filter(photos_count__gt=3).count()

        # Store data points
        Metric.insert_metric(Metric.KPI_TOTAL_RECIPES_3_PHOTOS, pivot_date, cnt_foodie_plus_3,
                             segment=Metric.SEG_FOODIES)
        Metric.insert_metric(Metric.KPI_TOTAL_RECIPES_3_PHOTOS, pivot_date, cnt_pro_plus_3,
                             segment=Metric.SEG_CHEFS)

        # Send data to Dashboard
        GeckoBoard.push_recipes_created(cnt_foodie_plus_3 + cnt_pro_plus_3, cnt_pro_plus_3, cnt_foodie_plus_3)

        self.stdout.write("%s Total foodies recipes created" % cnt_foodie)
        self.stdout.write("%s Total chefs recipes created" % cnt_pro)
        self.stdout.write("%s foodies recipes with more than 3 photos" % cnt_foodie_plus_3)
        self.stdout.write("%s chefs recipes with more than 3 photos" % cnt_pro_plus_3)
