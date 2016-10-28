# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

from chefs.models import Chefs
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Send fake PUSH notifications to staff users'
    option_list = BaseCommand.option_list + (
        make_option('--follower',
                    action='store',
                    help='email of follower'),
        make_option('--followed',
                    action='store',
                    help='email of followed'),
    )

    def handle(self, *args, **options):
        if not options['follower']:
            self.stderr.write("You must specify an email of follower user")
            return

        try:
            follower = Chefs.objects.get(email=options['follower'])
        except Chefs.DoesNotExist:
            self.stderr.write("Follower email %s does not exist" % options['follower'])
            return

        if not options['followed']:
            self.stderr.write("You must specify an email of followed user")
            return

        try:
            followed = Chefs.objects.get(email=options['followed'])
        except Chefs.DoesNotExist:
            self.stderr.write("Followed email %s does not exist" % options['followed'])
            return

        # Send following notification
        Notification.create_new_follow(followed, follower)

        self.stdout.write("End of test")
