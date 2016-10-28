import json
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext as _
from django.utils.translation import gettext_noop
from django.utils.timezone import now

from chefs.models import Chefs
from recipe.models import Comments, Recipes
from utils.common import get_redis


def _get_alert(payload, language):
    cur_language = translation.get_language()
    translation.activate(language)

    strings = {
        'follow': _('%(creator_name)s is now following you.'),
        'comment': _('%(creator_name)s has commented on your %(recipe_title)s.'),
        'like': _('%(creator_name)s loves your %(recipe_title)s.'),
        'copy_recipe': _('%(creator_name)s has added your %(recipe_title)s.'),
        'comment_reply': _("%(creator_name)s has commented on %(recipe_title)s."),
        'friend_follow': _("%(creator_name)s is now following %(followed)s."),
        'friend_published': _('%(creator_name)s has published %(recipe_title)s.')
    }
    string = strings.get(payload['type'])

    d = {}
    chef = Chefs.objects.get(pk=payload['creator_id'])
    d['creator_name'] = chef.get_full_name()

    if 'recipe_id' in payload:
        recipe = Recipes.objects.get(pk=payload['recipe_id'])
        d['recipe_title'] = recipe.name

    if 'followed_id' in payload:
        followed = Chefs.objects.get(pk=payload['followed_id'])
        d['followed'] = followed.get_full_name()

    ret = string % d
    translation.activate(cur_language)
    return ret


def send_message_to_devices(chef, payload):
    r = get_redis()

    for device in chef.devices.all():
        try:
            alert = _get_alert(payload, device.language)
        except:
            continue

        message = {
            'os_type': device.type,
            'environment': device.environment,
            'devices': [device.identificator],
            'alert': alert,
            'payload': payload,
        }
        r.rpush('cookbooth', json.dumps(message))


class NotificationType(models.Model):
    name = models.CharField(max_length=50)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_types'

    def __unicode__(self):
        return self.name


class NotificationManager(models.Manager):
    def unread(self):
        queryset = self.filter(unread=True, creation_date__lte=now())
        return queryset


class Notification(models.Model):
    unread = models.BooleanField(default=True)
    message = models.CharField(max_length=140, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    chef = models.ForeignKey(Chefs, blank=True, null=True, related_name='notifications')    # recipient for notification
    creator = models.ForeignKey(Chefs, blank=True, null=True, related_name='notifications_author')
    recipe = models.ForeignKey(Recipes, blank=True, null=True)
    type = models.ForeignKey(NotificationType, db_column='type', blank=True, null=True)
    comment = models.ForeignKey(Comments, blank=True, null=True)
    followed = models.ForeignKey(Chefs, blank=True, null=True)

    code = models.CharField(max_length=20, blank=True, null=True)
    deeplink = models.CharField(max_length=255, blank=True, null=True)

    objects = NotificationManager()

    class Meta:
        db_table = 'notifications'

    def __unicode__(self):
        return u"%s %s %s" % (self.creator, self.type, self.chef)

    @classmethod
    def create_new_follow(cls, followed, follower):
        """
        Create and sent notification of type 'follow'
        """
        type_, __ = NotificationType.objects.get_or_create(name='follow')
        notification = Notification.objects.create(type=type_, chef=followed, creator=follower)
        payload = {'id': notification.pk, 'type': 'follow', 'creator_id': follower.pk}
        send_message_to_devices(notification.chef, payload)

    @classmethod
    def send_new_friend_follow(cls, followed, follower):
        """
        Send a notifications to follower friends about new follow
        """
        type_, __ = NotificationType.objects.get_or_create(name='friend_follow')

        # notify to follower friends
        for friend in follower.followers.all():
            if friend.pk == followed.pk:
                continue
            notification = Notification.objects.create(type=type_,
                                                       chef=friend,
                                                       creator=follower,
                                                       followed=followed)
            payload = {
                'id': notification.pk,
                'type': 'friend_follow',
                'creator_id': follower.pk,
                'friend_id': friend.pk,
                'followed_id': followed.pk
            }
            send_message_to_devices(friend, payload)

    @classmethod
    def create_new_comment(cls, comment):
        """
        Create and sent notification of type 'comment'
        """
        type_, __ = NotificationType.objects.get_or_create(name='comment')
        notification = Notification.objects.create(
            type=type_,
            comment=comment,
            recipe=comment.recipe,
            chef=comment.recipe.chef,
            creator=comment.chef
        )
        payload = {
            'id': notification.pk,
            'type': 'comment',
            'creator_id': notification.creator.pk,
            'recipe_id': notification.recipe.pk,
            'comment_id': notification.comment.pk,
        }
        send_message_to_devices(notification.chef, payload)

    @classmethod
    def send_new_comment_to_thread(cls, comment):
        """
        Send a notification to all users in recipe comment threads
        """
        type_, __ = NotificationType.objects.get_or_create(name='comment_reply')

        # Get comments of the commented recipe, excluding comments by same author
        comments = Comments.objects.filter(recipe=comment.recipe)\
            .exclude(chef=comment.chef)\
            .exclude(chef=comment.recipe.chef)

        # Send to every user, only once
        already_sent = []
        for c in comments:
            if c.chef.pk not in already_sent:
                already_sent.append(c.chef.pk)
                notification = Notification.objects.create(
                    type=type_,
                    comment=comment,
                    recipe=comment.recipe,
                    chef=c.chef,
                    creator=comment.chef
                )
                payload = {
                    'id': notification.pk,
                    'type': 'comment_reply',
                    'creator_id': notification.creator.pk,
                    'recipe_id': notification.recipe.pk,
                    'comment_id': notification.comment.pk,
                }
                send_message_to_devices(notification.chef, payload)


    @classmethod
    def create_new_like(cls, like):
        """
        Create and sent notification of type 'like'
        """
        type_, __ = NotificationType.objects.get_or_create(name='like')
        notification = Notification.objects.create(
            type=type_,
            recipe=like.recipe,
            chef=like.recipe.chef,
            creator=like.chef
        )
        payload = {
            'id': notification.pk,
            'type': 'like',
            'creator_id': notification.creator.pk,
            'recipe_id': notification.recipe.pk,
        }
        send_message_to_devices(notification.chef, payload)

    @classmethod
    def create_new_copy_recipe(cls, recipe, chef):
        """
        Create and sent notification of type 'copy_recipe'
        """
        type_, __ = NotificationType.objects.get_or_create(name='copy_recipe')
        notification = Notification.objects.create(
            type=type_,
            recipe=recipe,
            chef=recipe.chef,
            creator=chef
        )
        payload = {
            'id': notification.pk,
            'type': 'copy_recipe',
            'creator_id': notification.creator.pk,
            'recipe_id': notification.recipe.pk,
        }
        send_message_to_devices(notification.chef, payload)

    @classmethod
    def create_new_recipe(cls, recipe):
        """
        Notify chef's followers of new recipe publication.
        """
        type_, __ = NotificationType.objects.get_or_create(name='friend_published')

        friends = recipe.chef.followers.all()
        for friend in friends:
            notification = Notification.objects.create(
                type=type_,
                recipe=recipe,
                chef=friend,
                creator=recipe.chef
            )
            payload = {
                'id': notification.pk,
                'type': 'friend_published',
                'creator_id': notification.creator.pk,
                'recipe_id': notification.recipe.pk,
            }
            send_message_to_devices(notification.chef, payload)


class Device(models.Model):
    type = models.CharField(max_length=10, blank=True)
    identificator = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=10, blank=True)
    environment = models.CharField(max_length=20, blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    chef = models.ForeignKey(Chefs, blank=True, null=True, related_name='devices')

    class Meta:
        db_table = 'devices'


class LocalNotificationsManager(models.Manager):
    def _get_messages(self, user, user_language, message_type):
        # Check for previous local notifications
        local_type, _ = NotificationType.objects.get_or_create(name='local')

        previous = Notification.objects.filter(creator=user, type=local_type)\
                               .values_list('code', flat=True)
        ids_to_exclude = list(previous)

        queryset = self.filter(language=user_language, message_type=message_type,)\
                       .exclude(pk__in=ids_to_exclude)\
                       .order_by('days')

        # Save local notifications in notifications history
        today = now()
        for ln in queryset:
            notification_date = today + timedelta(days=ln.days)
            n = Notification.objects.create(unread=True,
                                            creator=user, chef=user,
                                            message=ln.message, deeplink=ln.deeplink,
                                            type=local_type, code=ln.pk)
            n.creation_date = notification_date     # creation_date is auto_now_add
            n.save()


        # This query need to be repeated due to previous iteration
        queryset = self.filter(language=user_language, message_type=message_type,)\
                       .exclude(pk__in=ids_to_exclude)\
                       .order_by('days')

        return queryset

    def messages_for_new_users(self, user, user_language='en'):
        return self._get_messages(user, user_language, LocalNotification.MESSAGE_FOR_NEW_USER)

    def messages_for_old_users(self, user, user_language='en'):
        return self._get_messages(user, user_language, LocalNotification.MESSAGE_FOR_OLD_USER)


class LocalNotification(models.Model):
    MESSAGE_FOR_NEW_USER = 'N'
    MESSAGE_FOR_OLD_USER = 'O'

    MESSAGE_TYPE_CHOICES = (
        (MESSAGE_FOR_NEW_USER, _('Message for new users')),
        (MESSAGE_FOR_OLD_USER, _('Message for old users')),
    )

    LANGUAGE_CHOICES = (
        ('en', gettext_noop('English')),
        ('es', gettext_noop('Spanish')),
        ('ca', gettext_noop('Catalan')),
        ('de', gettext_noop('Deutch')),
        ('fr', gettext_noop('French')),
        ('pt', gettext_noop('Portuguese')),
    )
    days = models.SmallIntegerField(default=1)
    language = models.CharField(max_length=7, default='en', choices=LANGUAGE_CHOICES)
    message_type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    message = models.CharField(max_length=255, blank=True, null=True)
    deeplink = models.CharField(max_length=255, blank=True, null=True)

    objects = LocalNotificationsManager()

    class Meta:
        db_table = 'notifications_local'
        unique_together = ('message_type', 'language', 'days')
        ordering = ('language', 'days')

    def __unicode__(self):
        return "Days after %s: %s" % (self.days, self.message)
