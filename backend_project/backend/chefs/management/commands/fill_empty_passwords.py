from random import randint

from django.core.management.base import BaseCommand
from chefs.models import Chefs


class Command(BaseCommand):
    """
    django need users with passwords informed, so we need to fill random password for
    legacy users or users logged with facebook.
    """
    def handle(self, *args, **options):
        alphabet = list("abcdefghijklmnopqrstuvwxyz" +
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

        users = Chefs.objects.filter(password__isnull=True)

        self.stdout.write("%s usuarios sin password" % users.count())
        k = 0
        for u in users:
            random_pass = "".join([alphabet[randint(0, len(alphabet)-1)] for i in range(0, 8)])
            self.stdout.write("Setting password %s for user %s" % (random_pass, u.email))
            u.set_password(random_pass)

            if u.last_login is None:
                u.last_login = u.creation_date

            u.save()
            k += 1

        self.stdout.write("%s usuarios actualizados." % k)