from chefs.models import Chefs
import datetime, copy

import random
import string

class ChefDataProvider:
    def __init__(self, chef = Chefs(
        email='user'.join( [random.choice(string.letters) for i in xrange(15)] ) + '@mail.com',
        username='user'.join( [random.choice(string.letters) for i in xrange(15)] ) + '@mail.com',
        name='user',
        surname='default',
        type=1,
        creation_date=datetime.datetime.now(),
        language='es',
        active=0,
        source='web',
        confirmation_email=0,
        cache_activity=0,
        cache_likes=0,
        cache_score=0,
        cache_activity_score=0,
        cache_recipes=0,
        cache_recipes_score=0,
        cache_photos_score=0,
        cache_photo_descriptions_score=0,
        cache_likes_score=0,
        noted=0,
        manual_score=0,
        final_score=0,
        email_newsletter = True,
        email_notifications = True
    )):
        self.chef = copy.deepcopy(chef)

    def build(self):
        return self.chef

    def withId(self, id):
        self.chef.id = id
        return self

    def withName(self, name):
        self.chef.name = name
        return self

    def withSurname(self, surname):
        self.chef.surname = surname
        return self

    def withEmail(self, email):
        self.chef.email = email
        return self

    def withMembership(self, membership):
        self.chef.membership = membership
        return self

    @staticmethod
    def get():
        return ChefDataProvider()

    @staticmethod
    def getDefault():
        data_provider = ChefDataProvider()
        return data_provider.build()
