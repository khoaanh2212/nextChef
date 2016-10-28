"""Common settings and globals."""

from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path, stdout, argv

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Site url
SITE_URL = 'http://nextchef.local:8001'

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Malwine', 'malwine.steinbock@nextchef.co'),
    ('Hello', 'hello@nextchef.co'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('MYSQL_DATABASE', 'cookbooth'),
        'USER': environ.get('MYSQL_USER', 'usr_cookbooth'),
        'PASSWORD': environ.get('MYSQL_PASSWORD', 'cookbooth'),
        'HOST': environ.get('MYSQL_HOST', 'nextchef.db'),
        'PORT': environ.get('MYSQL_PORT', '3306'),
        'STORAGE_ENGINE': 'INNODB'
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = (normpath(join(SITE_ROOT, 'locale')),)
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

########## DYNAMIC FILE UPLOAD
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
)
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 6
########## END DYNAMIC FILE UPLOAD

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"tfze2a9@9wan)bqx94c((k7yum&kolo+nab!7w9x$ts17wv-ex"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'backend.context_processors.facebook_app_id',
    'backend.context_processors.debug',
    'backend.context_processors.user_avatar',
    'backend.context_processors.collections',
    'backend.context_processors.user_loves',
    'backend.context_processors.user_followings',
    'backend.context_processors.stripe',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    # 'api_utils.middleware.ApiDomainMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'grappelli',  # Grappelli need to be included before admin
    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'rest_framework',
    'easy_thumbnails',
    'django_like',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'books',
    'registration',
    'chefs',
    'recipe',
    'explore',
    'library',
    'landing',
    'notifications',
    'metrics',
    'products',
    'banners',
    'colls',
    'emailing',
    'subscribers',
    'unit_tests',
    'integration_tests',
    'costing'
)

# Apps specific for this project go here.
CONFIG_APPS = (
    'application',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + CONFIG_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG' if environ.get('DEBUG', 'false') == 'true' else 'INFO',
            'class': 'logging.StreamHandler',
            'stream': stdout
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION

########## SOUTH CONFIGURATION
# See: http://south.readthedocs.org/en/latest/installation.html#configuring-your-django-installation
INSTALLED_APPS += (
    # Database migration helpers:
    'south',
)
# Don't need to use South when setting up a test database.
SOUTH_TESTS_MIGRATE = True

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}
########## END SOUTH CONFIGURATION

########## EASY_THUMBNAILS CONFIGURATION
# See: http://easy-thumbnails.readthedocs.org/en/2.1/ref/settings/#easy_thumbnails.conf.Settings.THUMBNAIL_ALIASES

# THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_BASEDIR = 'thumbs'
# THUMBNAIL_DEBUG = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'easy_thumbnails.processors.filters',
    'easy_thumbnails.processors.background',
)

THUMBNAIL_ALIASES = {
    'books.Book.image': {
        'explore_box': {
            'size': (380, 300),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'recipe.Recipes.cover_image': {
        'explore_cover': {
            'size': (1280, 460),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'library_cover': {
            'size': (1070, 450),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'embed_cover': {
            'size': (600, 307),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'wordpress_header': {
            'size': (886, 400),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'email_header': {
            'size': (600, 250),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'library_edit_modal_cover': {
            'size': (598, 180),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'chefs_box': {
            'size': (534, 286),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'explore_box': {
            'size': (380, 300),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'email_cover': {
            'size': (270, 152),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'kitchen_book_cover': {
            'size': (110, 100),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'global_search': {
            'size': (70, 70),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'share_facebook': {
            'size': (1200, 630),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'recipe.Photos.image_url': {
        'recipe_step_full_size': {
            'size': (765, 500),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'publish_email_size': {
            'size': (198, 132),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'recipe_step': {
            'size': (390, 278),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'kitchen_edit': {
            'size': (375, 278),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'chef_avatar': {
            'size': (130, 130),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'kitchen_drag': {
            'size': (124, 92),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'explore_avatar': {
            'size': (94, 94),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'base_nav_avatar': {
            'size': (50, 50),
            'quality': 85,
            'crop': True,
            'upscale': True,
        }
    },
    'chefs.Chefs.cover': {
        'library_cover': {
            'size': (1070, 450),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'library_edit_modal_cover': {
            'size': (598, 180),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'email_header': {
            'size': (600, 250),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'explore_box': {
            'size': (380, 300),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'chefs.Restaurant.image': {
        'library_restaurant_cover': {
            'size': (1280, 460),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'account_button': {
            'size': (342, 122),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'products.Product.banner_image': {
        'banner_explore_thumb': {
            'size': (288, 452),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'products.ProductImage.photo': {
        'product_app_thumb': {
            'size': (400, 212),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'banners.Banner.image': {
        'banner_explore_thumb': {
            'size': (288, 452),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
    'colls.Collection.cover': {
        'collection_header_thumb': {
            'size': (1280, 340),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
        'facebook_thumb': {
            'size': (380, 300),
            'quality': 85,
            'crop': True,
            'upscale': True,
        },
    },
}

########## END EASY_THUMBNAILS CONFIGURATION

########## REST_FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'PAGINATE_BY': 12,  # Default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'MAX_PAGINATE_BY': 100,

    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'api_utils.renderers.CookboothRenderer',
    )
}
########## END REST_FRAMEWORK CONFIGURATION

##### REDIS BASED SESSION STORAGE ####
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
##### END REDIS BASED SESSION STORAGE ####

##### DJANGO REGISTRATION CONFIGURATION ####
AUTH_USER_MODEL = "chefs.Chefs"
LOGIN_REDIRECT_URL = '/library/profile/'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', 'chefs.backends.auth.EmailAuthBackend',)
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
##### END DJANGO REGISTRATION CONFIGURATION ####

##### DJANGO AMAZON S3 CONFIGURATION ####
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = 'AKIAIDDTKFEWCJYR2QOQ'
AWS_SECRET_ACCESS_KEY = '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'
##### END DJANGO AMAZON S3 CONFIGURATION ####

########## GECKOBOARD CONFIGURATION
GB_DISABLED = True  # Disable Geckoboard API calls
GB_API_KEY = ""
########## END GECKOBOARD CONFIGURATION

##### FULL URLS ####
SHARE_URL = 'http://nextchef.co/recipe/'
##### END FULL URLS ####


##### REDIS CONFIGURATION ####
REDIS_HOST = 'nextchef.redis'
REDIS_PORT = 6379
REDIS_DB = 5
##### END REDIS CONFIGURATION ####


########## ELASTICSEARCH CONFIGURATION
ES_URLS = ['nextchef.elasticsearch:9200']
ES_INDEXES = {'default': 'cookbooth'}
########## END ELASTICSEARCH CONFIGURATION


########## MAILING AND LISTS CONFIGURATION
SUBSCRIBE_TO_LISTS = True
SENDY_LISTS = {
    'en': {'pro': '892ZGLGFqDAGEori7Vfgu763rg', 'foodie': 'AsanVRZBpyrM2oiBPOgF3Q'},
    'es': {'pro': '5lAwcLRcrgL3nqr0t7HSOg', 'foodie': 'eRx0EWjrRy9rMuLdnNhHaw'}}
SENDY_URL = 'http://mailing.nextchef.co'
########## END MAILING AND LISTS CONFIGURATION

########## EVENT & METRICS CONFIGURATION
TRACK_EVENTS = True
MIN_SEARCH_TRACK = 6  # Don't track search events with less than this value
########## END EVENT & METRICS CONFIGURATION

########## GRAPPELLI ADMIN CONFIGURATION
GRAPPELLI_ADMIN_TITLE = 'Nextchef Admin'
GRAPPELLI_AUTOCOMPLETE_LIMIT = 10
########## END GRAPPELLI ADMIN CONFIGURATION

########## GEOIP CREDENTIALS
GEOIP_USER = 96918
GEOIP_KEY = None  # Disabled in not production environments
########## END GEOIP CREDENTIALS

########## STRIPE CONFIG
STRIPE_SUBSCRIPTION_UPDATE = 'customer.subscription.updated'
########## END STRIPE CONFIG

########## EDAMAM CONFIG
EDAMAM_NUTRITION_API = 'https://api.edamam.com/api/nutrition-data'
EDAMAM_RECIPE_ANALYZE_API = 'https://api.edamam.com/api/nutrition-details'
# EDAMAM_APP_ID = 'e343499f'
# EDAMAM_APP_KEY = '1942903827d08b20e3a4585bd955968e'
EDAMAM_APP_ID = 'd988f4dd'
EDAMAM_APP_KEY = '4e072cea03600962fa01ce6e447682a4'
EDAMAM_NUTRITION_DATA_API_KEY = '368e4f6d2cc3773c2c74271620e02be2'

########## END EDAMAM CONFIG

########## ALLERGENS
GLUTEN = 'gluten'
CRUSTACEANS = 'crustaceans'
EGGS = 'eggs'
FISH = 'fish'
PEANUTS = 'peanuts'
SOYBEANS = 'soybeans'
MILK = 'milk'
NUTS = 'nuts'
CELERY = 'celery'
MUSTARD = 'mustard'
SESAME = 'sesame'
LUPINE = 'lupine'
MOLLUSKS = 'mollusks'
########## END OF ALLERGENS

########## NC ALLERGENS
NC_GLUTEN = 'Gluten'
NC_CRUSTACEANS = 'Crustaceans'
NC_EGGS = 'Eggs'
NC_FISH = 'Fish'
NC_PEANUTS = 'Peanuts'
NC_SOYBEANS = 'Soybeans'
NC_MILK = 'Milk'
NC_NUTS = 'Nuts'
NC_CELERY = 'Celery'
NC_MUSTARD = 'Mustard'
NC_SESAME = 'Sesame'
NC_LUPINE = 'Lupine'
NC_MOLLUSKS = 'Mollusks'
########## END OF NC ALLERGENS

########## EDAMAM ALLERGENS
EDAMAM_GLUTEN = 'GLUTEN_FREE'
EDAMAM_CRUSTACEANS = 'CRUSTACEAN_FREE'
EDAMAM_EGGS = 'EGG_FREE'
EDAMAM_FISH = 'FISH_FREE'
EDAMAM_PEANUTS = 'PEANUT_FREE'
EDAMAM_SOYBEANS = 'SOY_FREE'
EDAMAM_MILK = 'MILK_FREE'
EDAMAM_NUTS = 'TREE_NUT_FREE'
EDAMAM_CELERY = 'CELERY_FREE'
EDAMAM_MUSTARD = 'MUSTARD_FREE'
EDAMAM_SESAME = 'SESAME_FREE'
EDAMAM_LUPINE = 'LUPINE_FREE'
EDAMAM_MOLLUSKS = 'MOLLUSK_FREE'
########## END EDAMAM ALLERGENS

########## ALLERGEN LIST
EDAMAM_ALLERGENS = (
    (GLUTEN, EDAMAM_GLUTEN),
    (CRUSTACEANS, EDAMAM_CRUSTACEANS),
    (EGGS, EDAMAM_EGGS),
    (FISH, EDAMAM_FISH),
    (PEANUTS, EDAMAM_PEANUTS),
    (SOYBEANS, EDAMAM_SOYBEANS),
    (MILK, EDAMAM_MILK),
    (NUTS, EDAMAM_NUTS),
    (CELERY, EDAMAM_CELERY),
    (MUSTARD, EDAMAM_MUSTARD),
    (SESAME, EDAMAM_SESAME),
    (LUPINE, EDAMAM_LUPINE),
    (MOLLUSKS, EDAMAM_MOLLUSKS)
)

NC_ALLERGENS = (
    (GLUTEN, NC_GLUTEN),
    (CRUSTACEANS, NC_CRUSTACEANS),
    (EGGS, NC_EGGS),
    (FISH, NC_FISH),
    (PEANUTS, NC_PEANUTS),
    (SOYBEANS, NC_SOYBEANS),
    (MILK, NC_MILK),
    (NUTS, NC_NUTS),
    (CELERY, NC_CELERY),
    (MUSTARD, NC_MUSTARD),
    (SESAME, NC_SESAME),
    (LUPINE, NC_LUPINE),
    (MOLLUSKS, NC_MOLLUSKS)
)
########## END ALLERGEN LIST

########## PAGE LIMIT

COSTING_PAGE_LIMIT = 500
INGREDIENT_SUGGESTION_LIMIT = 5
RECIPE_SUGGESTION_LIMIT = 5

########## END PAGE LIMIT

UNIT_KG = 'kg'
UNIT_LBS = 'lbs'

KG_TO_LBS = 2.20462
GR_TO_KG = 0.001

TESTING = len(argv) > 1 and argv[1] == 'test'
