from __future__ import absolute_import

from backend.settings.base import *

DATABASES['default']['ENGINE'] = environ.get('TEST_DB_ENGINE', 'django.db.backends.sqlite3')
DATABASES['default']['NAME'] = environ.get('TEST_DB_NAME', ':memory:')

ALLOWED_HOSTS = ['testserver']

########## DISABLE MIGRATIONS
# See: https://south.readthedocs.org/en/latest/settings.html#south-tests-migrate
#SOUTH_TESTS_MIGRATE = False
########## END DISABLE MIGRATIONS

########## ELASTICSEARCH CONFIGURATION
ES_DISABLED = True  # Disabled in tests
########## END ELASTICSEARCH CONFIGURATION

########## STRIPE CONFIGURATION
STRIPE_KEY_SECRET = "sk_live_sSvXAKgKNNMA5SFXWpUrVpmv"
STRIPE_KEY_PUBLIC = "pk_live_O5RK8WVMFYpMrNgMJQFUKZxb"
########## END STRIPE CONFIGURATION

FACEBOOK_APP_ID = ""

# SMTP Stub
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
