import binascii
import os

import facebook
from rest_framework import serializers

from api_utils.fields import Base64ImageField, IntegerBooleanField
from api_utils.pagination import CookboothPaginationSerializer
from api_utils.serializers import CookboothModelSerializer, datetime_to_timestamp

from utils.email import send_activation_email, subscribe_sendy, send_welcome_email, subscribe_sendy

from .models import Chefs


class ChefsSerializer(serializers.ModelSerializer):
    type_class = serializers.Field('type_class')
    cover = serializers.Field('thumb_chefs_box')
    photo = serializers.Field('photo')
    url = serializers.Field('url')
    full_name = serializers.Field('full_name')
    loves = serializers.Field('cache_likes')

    class Meta:
        model = Chefs
        fields = ('id', 'url', 'cover', 'full_name', 'photo', 'loves', 'short_bio' , 'location',
                  'type_class')


class ApiChefsSerializer(CookboothModelSerializer):
    # Overwrite password so it is not required
    password = serializers.CharField('password', write_only=True, required=False)
    offline = IntegerBooleanField()
    private_recipes = IntegerBooleanField()
    photo = Base64ImageField(required=False)
    cover = Base64ImageField(required=False)
    nb_followings = serializers.Field('nb_followings')
    nb_followers = serializers.Field('nb_followers')
    nb_books = serializers.Field('nb_books')
    nb_recipes = serializers.Field('nb_recipes')
    nb_likes = serializers.Field('nb_likes')

    class Meta:
        model = Chefs
        fields = ('id', 'email', 'password', 'username', 'name', 'surname', 'type', 'language',
                  'languages', 'country', 'location', 'interests', 'referents', 'short_bio',
                  'level', 'fb_access_token', 'private_recipes', 'offline', 'photo', 'cover',
                  'edit_date', 'creation_date', 'nb_followings', 'nb_followers', 'nb_books',
                  'nb_recipes', 'nb_likes')
        read_only_fields = ('edit_date', 'creation_date')
        write_only_fields = ('country', 'location', 'interests', 'referents',
                             'short_bio', 'level', 'fb_access_token')

    def transform_photo(self, obj, value):
        try:
            photo = obj.avatar_photos.all()[0]
            if photo:
                if 'http' in photo.s3_url.name:
                    photo_url = photo.s3_url.name
                else:
                    photo_url = photo.s3_url.url
            else:
                photo_url = ""
            return {
                'id': photo.pk,
                'url': photo_url,
                'creation_date': self.datetime_to_timestamp(photo.creation_date),
                'edit_date': self.datetime_to_timestamp(photo.edit_date),
            }
        except:
            return None

    def transform_cover(self, obj, value):
        return obj.cover_thumb('explore_box')

    def transform_interests(self, obj, value):
        return obj.interests if obj.interests else ""

    def transform_referents(self, obj, value):
        return obj.referents if obj.referents else ""

    def transform_languages(self, obj, value):
        return obj.languages.split(' ') if obj.languages else []

    def transform_type(self, obj, value):
        if obj.type == 0 or obj.type is None:
            return Chefs.TYPE_FOODIE
        else:
            return Chefs.TYPE_PRO

    def validate_password(self, attrs, source):
        if source not in attrs:
            return attrs
        if not attrs[source].strip():
            raise serializers.ValidationError("Blank passwords are not allowed")
        self._password_change = True
        return attrs

    def validate_fb_access_token(self, attrs, source):
        fb_access_token = attrs.get('fb_access_token')
        if not fb_access_token:
            return attrs
        try:
            graph = facebook.GraphAPI(fb_access_token)
            profile = graph.get_object("me")
            attrs['fb_user_id'] = profile['id']
        except facebook.GraphAPIError:
            raise serializers.ValidationError("Not valid Facebook access token")
        return attrs

    def validate_languages(self, attrs, source):
        langs = attrs.get('languages', '').split(' ')
        langs = set(l for l in langs if l in Chefs.LANGUAGES_CHOICES)
        attrs['languages'] = ' '.join(langs)
        return attrs

    def validate(self, attrs):
        """
        Check that either password or fb_access_token are supplied on creation
        and set defaults in object creation
        """
        # If object is new
        if self.object is None:
            if not attrs.get('password'):
                if not attrs.get('fb_access_token'):
                    raise serializers.ValidationError("A password or fb_access_token is required")

                # Set a random password
                attrs['password'] = binascii.hexlify(os.urandom(20)).decode()
                self._password_change = True
            attrs['source'] = 'api'
        return attrs

    def restore_object(self, attrs, instance=None):
        self._photo = attrs.pop('photo', None)
        return super(ApiChefsSerializer, self).restore_object(attrs, instance)

    def save_object(self, obj, **kwargs):
        is_new = self.object.pk is None
        if getattr(self, '_password_change', False):
            obj.api_set_password(obj.password)
        obj.save(**kwargs)

        if self._photo:
            obj.photo = self._photo
        if is_new:
            if obj.fb_user_id:
                send_welcome_email(obj)
            else:
                send_activation_email(obj)
            subscribe_sendy(obj)

    def to_native(self, obj):
        ret = super(ApiChefsSerializer, self).to_native(obj)
        if not ret['photo']:
            del ret['photo']
        return ret


class ApiChefsViewSerializer(ApiChefsSerializer):
    """
    Used in GET requests
    """
    most_popular_recipe_cover_image = serializers.SerializerMethodField('get_popular_cover')
    short_bio = serializers.SerializerMethodField('get_short_bio')

    class Meta:
        model = Chefs
        fields = ('id', 'email', 'username', 'name', 'surname', 'type', 'language', 'languages',
                  'country', 'location', 'interests', 'referents', 'short_bio', 'private_recipes',
                  'offline', 'photo', 'cover', 'edit_date', 'creation_date', 'nb_followings',
                  'nb_followers', 'nb_books', 'nb_recipes', 'nb_likes',
                  'most_popular_recipe_cover_image')
        read_only_fields = ('edit_date', 'creation_date')

    def transform_location(self, obj, value):
        return obj.location if obj.location else ""

    def transform_interests(self, obj, value):
        return obj.interests if obj.interests else ""

    def transform_referents(self, obj, value):
        return obj.referents if obj.referents else ""

    def get_short_bio(self, obj):
        return obj.short_bio if obj.short_bio else ""

    def get_popular_cover(self, obj):
        if not self.context.get('most_popular_recipe_cover_image') is True:
            return None
        photo = obj.most_popular_recipe_cover_image
        if photo:
            if 'http' in photo.s3_url.name:
                photo_url = photo.s3_url.name
            else:
                photo_url = photo.s3_url.url

            return {
                'id': photo.pk,
                'url': photo_url,
                'creation_date': self.datetime_to_timestamp(photo.creation_date),
                'edit_date': self.datetime_to_timestamp(photo.edit_date),
            }
        else:
            return None

    def to_native(self, obj):
        ret = super(ApiChefsViewSerializer, self).to_native(obj)
        if not ret['most_popular_recipe_cover_image']:
            del ret['most_popular_recipe_cover_image']
        return ret


def embeded_chef_serializer(chef):
    ret = {
        'id': chef.pk,
        'type': 1 if chef.type else 0,
        'email': chef.email,
        'name': chef.name,
        'surname': chef.surname}

    try:
        photo = chef.avatar_photos.all()[0]
        if photo:
            if 'http' in photo.s3_url.name:
                photo_url = photo.s3_url.name
            else:
                photo_url = photo.s3_url.url
        else:
            photo_url = ""

        ret['photo'] = {
            'id': photo.pk,
            'url': photo_url,
            'creation_date': datetime_to_timestamp(photo.creation_date),
            'edit_date': datetime_to_timestamp(photo.edit_date),
        }
    except:
        pass
    return ret


class ApiChefsViewPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'chefs'


class APIV1ChefsSerializer(CookboothModelSerializer):
    type_class = serializers.Field('type_class')
    url = serializers.Field('url')
    avatar = serializers.SerializerMethodField('get_avatar_thumb')
    cover = serializers.SerializerMethodField('get_cover_thumb')
    nb_followers = serializers.Field('nb_followers')
    nb_loves = serializers.Field('nb_likes')
    full_name = serializers.Field('full_name')

    class Meta:
        model = Chefs
        fields = ('id', 'url', 'full_name', 'type_class', 'role', 'nb_followers', 'nb_loves',
                  'avatar', 'cover', 'location')

    def get_cover_thumb(self, obj):
        return obj.cover_thumb('explore_box')

    def get_avatar_thumb(self, obj):
        return obj.avatar_thumb('explore_avatar')

    def transform_location(self, obj, value):
        return obj.location if obj.location else ""


class APIV1EmbedChefSerializer(CookboothModelSerializer):
    full_name = serializers.Field('full_name')
    avatar = serializers.Field('thumb_chefs_nav_avatar')
    type_class = serializers.Field('type_class')

    class Meta:
        model = Chefs
        fields = ('id', 'full_name', 'avatar', 'type_class')


class ApiV1ByTypePaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'foodies'

    def to_native(self, obj):
        ret = super(ApiV1ByTypePaginatedSerializer, self).to_native(obj)

        page = self.object.number - 1
        start = page * self.object.paginator.per_page
        end = start + self.object.paginator.per_page
        serializer = self.opts.object_serializer_class

        ret['pros'] = [serializer(o).data for o in self.context['pros'][start:end]]
        ret['brands'] = [serializer(o).data for o in self.context['brands'][start:end]]
        return ret
