import json
from django.conf import settings
from django.core.cache import get_cache
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from backend.cache_utils import CacheUtils
from colls.models import Collection


def facebook_app_id(request):
    return {'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID}


def debug(context):
    return {'DEBUG': settings.DEBUG}


def user_avatar(request):
    avatar = None
    if request.user.is_authenticated():
        cache = get_cache('default')
        key = CacheUtils.get_key(CacheUtils.USER_AVATAR, user_id=request.user.id)
        avatar = cache.get(key, None)
        if avatar is None:
            avatar = thumbnail_url(request.user.avatar, 'base_nav_avatar')
            cache.set(key, avatar)
    return {'USER_AVATAR': avatar}


def collections(context):
    cache = get_cache('default')
    key = CacheUtils.get_key(CacheUtils.COLLECTIONS)
    colls = cache.get(key, None)
    if colls is None:
        colls = Collection.objects.filter(is_active=True).order_by('name')
        cache.set(key, colls)
    return {'COLLECTIONS': colls}


def user_loves(request):
    user_loves_json = []
    if request.user.is_authenticated():
        cache = get_cache('default')
        key = CacheUtils.get_key(CacheUtils.USER_LOVES, user_id=request.user.id)
        user_loves_json = cache.get(key, None)
        if user_loves_json is None:
            user_loves_json = json.dumps(request.user.loves_list)
            cache.set(key, user_loves_json)

    return {'USER_LOVES_LIST': user_loves_json}


def user_followings(request):
    user_followings_json = []
    if request.user.is_authenticated():
        cache = get_cache('default')
        key = CacheUtils.get_key(CacheUtils.USER_FOLLOWINGS, user_id=request.user.id)
        user_followings_json = cache.get(key, None)
        if user_followings_json is None:
            user_followings_json = json.dumps(request.user.follows_list)
            cache.set(key, user_followings_json)

    return {'USER_FOLLOWINGS_LIST': user_followings_json}

def stripe(request):
    return { 'STRIPE_KEY_PUBLIC': settings.STRIPE_KEY_PUBLIC }
