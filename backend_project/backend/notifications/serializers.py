from rest_framework import serializers

from api_utils.fields import IntegerBooleanField
from api_utils.pagination import CookboothPaginationSerializer
from api_utils.serializers import CookboothModelSerializer
from chefs.serializers import embeded_chef_serializer

from .models import Device, Notification, LocalNotification


class ApiDeviceSerializer(CookboothModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'type', 'identificator', 'language',
                  'environment')
        read_only_fields = ('chef', 'edit_date', 'creation_date')

    def transform_chef(self, obj, value):
        return {
            'id': obj.chef.pk,
            'type': obj.chef.type,
            'email': obj.chef.email,
            'name': obj.chef.name,
            'surname': obj.chef.surname}

    def save_object(self, obj, **kwargs):
        obj.chef = self.user
        super(ApiDeviceSerializer, self).save_object(obj, **kwargs)


class ApiDevicePaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'devices'


class ApiNotificationSerializer(CookboothModelSerializer):
    unread = IntegerBooleanField(source='unread')

    class Meta:
        model = Notification
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'creator', 'recipe', 'type',
                  'comment', 'unread', 'message', 'deeplink', 'followed')

        read_only_fields = ('creation_date', 'edit_date', 'chef', 'creator', 'recipe', 'type',
                            'comment', 'deeplink', 'followed')

    def transform_message(self, obj, value):
        return value if value is not None else ''

    def transform_type(self, obj, value):
        if not obj.type:
            return None

        return {
            'id': obj.type.pk,
            'creation_date': self.datetime_to_timestamp(obj.type.creation_date),
            'edit_date': self.datetime_to_timestamp(obj.type.edit_date),
            'name': obj.type.name}

    def transform_chef(self, obj, value):
        if not obj.chef:
            return None
        return embeded_chef_serializer(obj.chef)

    def transform_creator(self, obj, value):
        if not obj.creator:
            return None
        return embeded_chef_serializer(obj.creator)

    def transform_followed(self, obj, value):
        if not obj.followed:
            return None
        return embeded_chef_serializer(obj.followed)

    def transform_recipe(self, obj, value):
        if not obj.recipe:
            return None

        return {
            'id': obj.recipe.pk,

            'added': False,
            'commented': False,
            'liked': False,
            'reported': False,
            'shared': False,

            'creation_date': self.datetime_to_timestamp(obj.recipe.creation_date),
            'edit_date': self.datetime_to_timestamp(obj.recipe.edit_date),

            'name': obj.recipe.name,
            'commensals': obj.recipe.commensals,
            'draft': 1 if obj.recipe.draft else 0,
            'private': 1 if obj.recipe.private else 0,
            'ingredients': [{'id': i.pk, 'name': i.name} for i in obj.recipe.ingredients.all()],
            'tags': [{'id': t.pk, 'name': t.name} for t in obj.recipe.tags.all()],

            'nb_added': obj.recipe.nb_added,
            'nb_comments': obj.recipe.nb_comments,
            'nb_likes': obj.recipe.nb_likes,
            'nb_shares': obj.recipe.nb_shares,

            'public_url': obj.recipe.public_url,
        }

    def transform_comment(self, obj, value):
        if not obj.comment:
            return None

        return {'id': obj.comment.pk}

    def to_native(self, obj):
        ret = super(ApiNotificationSerializer, self).to_native(obj)
        for field in 'chef', 'creator', 'recipe', 'comment':
            if not ret[field]:
                del ret[field]
        return ret


class ApiNotificationPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'notifications'


class ApiLocalNotificationSerializer(CookboothModelSerializer):
    class Meta:
        model = LocalNotification
        fields = ('days', 'message', 'deeplink')

    def transform_deeplink(self, obj, value):
        return value if value is not None else ''
