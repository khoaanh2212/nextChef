# -*- coding: utf-8 -*-
from __future__ import division

from optparse import make_option
from datetime import datetime, time
from django.utils.timezone import utc
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand

from chefs.models import ChefFollows, Chefs
from recipe.models import Likes, Shares, Comments, Recipes


class Command(BaseCommand):
    help = 'Count social actions (follow, love, save, comment.'
    option_list = BaseCommand.option_list + (
        make_option('--date',
                    action='store',
                    dest='date_from',
                    default=None,
                    help='Get data from this date'),
        make_option('--days',
                    action='store',
                    dest='num_days',
                    default=None,
                    help='Get data to this date'),
    )

    def handle(self, *args, **options):
        if options['date_from']:
            pivot_date = datetime.strptime(options['date_from'], '%Y-%m-%d')
        else:
            self.stderr.write("La fecha de inicio es obligatoria")
            return

        if options['num_days']:
            num_days = int(options['num_days'])
        else:
            num_days = 91

        data = {}
        for single_date in (pivot_date - timedelta(n) for n in range(num_days)):
            pivot_date_min = datetime.combine(single_date, time(0, 0, 0, 0, tzinfo=utc))
            pivot_date_max = datetime.combine(single_date, time(23, 59, 59, 999999, tzinfo=utc))

            data[pivot_date] = {
                'active_users': [],
                'shares_chefs': [],
                'shares_foodies': [],
                'comment_chefs': [],
                'comment_foodies': [],
                'likes_chefs': [],
                'likes_foodies': [],
                'recipes_chefs': [],
                'recipes_foodies': [],
                'follows_chefs': [],
                'follows_foodies': []
            }
            active_chefs = []
            active_foodies = []
            active_users = []

            # Registered users (foodies & pros)
            registered_foodies = list(Chefs.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))
                                      .exclude(type=Chefs.TYPE_PRO)
                                      .values_list('id', flat=True))
            active_users += registered_foodies
            active_foodies += registered_foodies

            registered_chefs = list(Chefs.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))
                                                 .filter(type=Chefs.TYPE_PRO)
                                                 .values_list('id', flat=True))
            active_users += registered_chefs
            active_chefs += registered_chefs

            # Number of shares
            shares_foodies = list(Shares.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                                        .exclude(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['shares_foodies'] = shares_foodies
            active_users += shares_foodies
            active_foodies += shares_foodies

            shares_chefs = list(Shares.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                .filter(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['shares_chefs'] = shares_chefs
            active_users += shares_chefs
            active_chefs += shares_chefs

            # Number of comments
            comment_foodies = list(Comments.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                .exclude(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['comment_foodies'] = comment_foodies
            active_users += comment_foodies
            active_foodies += comment_foodies

            comment_chefs = list(Comments.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                .filter(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['comment_chefs'] = comment_chefs
            active_users += comment_chefs
            active_chefs += comment_chefs

            # Number of likes
            likes_foodies = list(Likes.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                                        .exclude(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['likes_foodies'] = likes_foodies
            active_users += likes_foodies
            active_foodies += likes_foodies

            likes_chefs = list(Likes.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                .filter(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['likes_chefs'] = likes_chefs
            active_users += likes_chefs
            active_chefs += likes_chefs

            # Recipes created
            recipes_foodies = list(Recipes.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                                        .exclude(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['recipes_foodies'] = recipes_foodies
            active_users += recipes_foodies
            active_foodies += recipes_foodies

            recipes_chefs = list(Recipes.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                .filter(chef__type=Chefs.TYPE_PRO).values_list('chef_id', flat=True))
            data[pivot_date]['recipes_chefs'] = recipes_chefs
            active_users += recipes_chefs
            active_chefs += recipes_chefs

            # Follows
            follows_foodies = list(ChefFollows.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                                        .exclude(follower__type=Chefs.TYPE_PRO).values_list('follower_id', flat=True))
            data[pivot_date]['follows_foodies'] = follows_foodies
            active_users += follows_foodies
            active_foodies += follows_foodies

            follows_chefs = list(ChefFollows.objects.filter(creation_date__range=(pivot_date_min, pivot_date_max))\
                                        .filter(follower__type=Chefs.TYPE_PRO).values_list('follower_id', flat=True))
            data[pivot_date]['follows_chefs'] = follows_chefs
            active_users += follows_chefs
            active_chefs += follows_chefs

            # Discard duplicates if exists any
            distinct_users = list(set(active_users))
            distinct_foodies = list(set(active_foodies))
            distinct_chefs = list(set(active_chefs))
            data[pivot_date]['active_users'] = distinct_users

            num_active_chefs = len(distinct_chefs)
            num_active_foodies = len(distinct_foodies)
            cnt_chefs_shares = len(shares_chefs)
            cnt_foodies_shares = len(shares_foodies)

            ratio_chefs = (cnt_chefs_shares / num_active_chefs) * 100
            ratio_foodies = (cnt_foodies_shares / num_active_foodies) * 100

            print single_date, cnt_chefs_shares, num_active_chefs, ratio_chefs, cnt_foodies_shares, num_active_foodies, ratio_foodies
