"""Development settings and globals."""

from __future__ import absolute_import

import dj_database_url

from .base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
# MANDRILL_API_KEY = "7wEB2F58pLIJJqjbDcXhPw"
########## END EMAIL CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.sparkpostmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '68b2f58f5641fd2a8b1b5252cd6df21a27cfa899')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'SMTP_Injection')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'no-reply@nextchef.co'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
########## END EMAIL CONFIGURATION


########## FACEBOOK CONFIGURATION
FACEBOOK_APP_ID = '1012849002132103'
FACEBOOK_APP_SECRET = '7f05a1b117a4d9e454e02615aefe26d5'
#FACEBOOK_CLIENT_TOKEN = '76f22a4a63a06e2abd5fd37812818e2d'
#FACEBOOK_APP_ID = '1012849002132103'
#FACEBOOK_APP_SECRET = '7f05a1b117a4d9e454e02615aefe26d5'
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


########## MAILING AND LISTS CONFIGURATION
SUBSCRIBE_TO_LISTS = False
########## END MAILING AND LISTS CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += ('djrill',)

MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION

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

######### CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 6000
    }
}
######### END CACHE CONFIGURATION

########## STRIPE CONFIGURATION
STRIPE_KEY_SECRET = "sk_live_sSvXAKgKNNMA5SFXWpUrVpmv"
STRIPE_KEY_PUBLIC = "pk_live_O5RK8WVMFYpMrNgMJQFUKZxb"
########## END STRIPE CONFIGURATION
