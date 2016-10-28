"""Development settings and globals."""

from __future__ import absolute_import

import dj_database_url

from .base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['.nextchef.co', 'api.test.cookbooth.com']
########## END HOST CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## FACEBOOK CONFIGURATION
FACEBOOK_APP_ID = '1012849002132103'
FACEBOOK_APP_SECRET = '7f05a1b117a4d9e454e02615aefe26d5'
FACEBOOK_SCOPE = 'email,publish_stream'
FACEBOOK_REGISTRATION_BACKEND = ''
########## END FACEBOOK CONFIGURATION

##### DJANGO AMAZON S3 CONFIGURATION ####
AWS_ACCESS_KEY_ID = 'AKIAIMXIM6HQCATYG5MQ'
AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIAFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_STORAGE_BUCKET_NAME = 'cookbooth-images-dev'
S3_URL = 'http://s3-eu-west-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
MEDIA_DIRECTORY = '/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY
MEDIA_ROOT = 'media/'
##### END DJANGO AMAZON S3 CONFIGURATION ####

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'OPTIONS': {
            'DB': 9,
        },
    },
}
########## END CACHE CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

########## MAILING AND LISTS CONFIGURATION
SUBSCRIBE_TO_LISTS = False
########## END MAILING AND LISTS CONFIGURATION

## throw all log into console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG' if environ.get('DEBUG', 'false') == 'true' else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

########## ELASTICSEARCH CONFIGURATION
ES_DISABLED = False
ES_URLS = ['nextchef.elasticsearch:9200']
ES_INDEXES = {'default': 'cookbooth'}
########## END ELASTICSEARCH CONFIGURATION


########## STRIPE CONFIGURATION
STRIPE_KEY_SECRET = "sk_live_sSvXAKgKNNMA5SFXWpUrVpmv"
STRIPE_KEY_PUBLIC = "pk_live_O5RK8WVMFYpMrNgMJQFUKZxb"
########## END STRIPE CONFIGURATION
