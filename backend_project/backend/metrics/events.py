from django.conf import settings

from mixpanel import Mixpanel


class Events(object):
    """
    Send events to Mixpanel
    """
    EVENT_SEARCH = 'search'
    EVENT_FOLLOW = 'follow_chef'
    EVENT_UNFOLLOW = 'unfollow_chef'
    EVENT_LOVE = 'recipe_love'
    EVENT_UNLOVE = 'recipe_unlove'
    EVENT_COMMENT = 'comment'
    EVENT_RECIPE_TO_BOOK = 'recipe_saved'
    EVENT_RECIPE_PUBLISH = 'recipe_publish'
    EVENT_RECIPE_PRIVATE = 'recipe_private'

    PROJECT_TOKEN = '9938ae03830ec73709d6631b414e205a'

    @staticmethod
    def track(user_id, event, properties=None):
        if not settings.TRACK_EVENTS:
            return

        data = {'source': 'web'}
        if properties:
            data = dict(data.items() + properties.items())

        mp = Mixpanel(Events.PROJECT_TOKEN)
        mp.track(user_id, event, data)
