"""Production settings and globals."""

from __future__ import absolute_import

from os import environ

from .base import *

import dj_database_url

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['.nextchef.co']
########## END HOST CONFIGURATION

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
SERVER_EMAIL = 'NextChef<hello@nextchef.co>'
DEFAULT_FROM_EMAIL = 'NextChef<no-reply@nextchef.co>'


'''
# Django_ses Module Configuration
EMAIL_BACKEND = 'django_ses.SESBackend'
# These are optional -- if they're set as environment variables they won't need to be set here as well
AWS_SES_ACCESS_KEY_ID = 'AKIAI4XJ7HCJA6D75EPQ'
AWS_SES_SECRET_ACCESS_KEY = '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'
AWS_SES_ACCESS_KEY_ID = 'AKIAIX56JLJ4WYHDO5LA'
AWS_SES_SECRET_ACCESS_KEY = 'Ar+KlyK/+qFaenC16fFjmxEKROru6D2kuFcIW2edGlFh'
#AWS_ACCESS_KEY_ID = 'AKIAIX56JLJ4WYHDO5LA'
#AWS_SECRET_ACCESS_KEY = 'Ar+KlyK/+qFaenC16fFjmxEKROru6D2kuFcIW2edGlFh'  
# Additionally, you can specify an optional region, like so:
AWS_SES_REGION_NAME = 'eu-west-1'
AWS_SES_REGION_ENDPOINT = 'email-smtp.eu-west-1.amazonaws.com'#'email.us-east-1.amazonaws.com'## #
'''

########## END EMAIL CONFIGURATION

########## FACEBOOK CONFIGURATION
FACEBOOK_APP_ID = '1012849002132103'
FACEBOOK_APP_SECRET = '7f05a1b117a4d9e454e02615aefe26d5'
FACEBOOK_SCOPE = 'email,publish_stream'
FACEBOOK_REGISTRATION_BACKEND = ''
########## END FACEBOOK CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
        'TIMEOUT': 3600,
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

##### DJANGO AMAZON S3 CONFIGURATION ####
AWS_ACCESS_KEY_ID = 'AKIAIDDTKFEWCJYR2QOQ'
AWS_SECRET_ACCESS_KEY = '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'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIAFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'cookbooth-images'
S3_URL = 'http://s3-eu-west-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
MEDIA_DIRECTORY = '/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY
MEDIA_ROOT = 'media/'

THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
##### END DJANGO AMAZON S3 CONFIGURATION ####

########## ELASTICSEARCH CONFIGURATION
ES_DISABLED = False
ES_URLS = ['nextchef.elasticsearch:9200']
ES_INDEXES = {'default': 'cookbooth'}
########## END ELASTICSEARCH CONFIGURATION

########## GECKOBOARD CONFIGURATION
GB_DISABLED = True  # Disable Geckoboard API calls
GB_API_KEY = "da53b462c8dc2ff28f726991d922ceb8"
########## END GECKOBOARD CONFIGURATION

########## EVENT & METRICS CONFIGURATION
TRACK_EVENTS = True     # Track events with mixpanel python library
########## END EVENT & METRICS CONFIGURATION

########## GEOIP CREDENTIALS
GEOIP_USER = 96918
GEOIP_KEY = 'jLjxBvStz8I2'
########## END GEOIP CREDENTIALS

########## STRIPE CONFIGURATION
STRIPE_KEY_SECRET = "sk_live_sSvXAKgKNNMA5SFXWpUrVpmv"
STRIPE_KEY_PUBLIC = "pk_live_O5RK8WVMFYpMrNgMJQFUKZxb"
########## END STRIPE CONFIGURATION
