import _mysql
import os
import time
from django.core.management import call_command
import logging
from time import sleep


def set_module_env_settings(settings):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings


def init(settings):
    set_module_env_settings(settings)
    result = None
    while result is None:
        try:
            # connect
            result = _mysql.connect(
                user=os.environ.get('MYSQL_USER', 'usr_cookbooth'),
                passwd=os.environ.get('MYSQL_PASSWORD', 'cookbooth'),
                host=os.environ.get('MYSQL_HOST', 'nextchef.db'),
                port=int(os.environ.get('MYSQL_PORT', '3306')),
                db=os.environ.get('MYSQL_DATABASE', 'cookbooth')
            )

        except Exception as e:
            logging.debug("%s" % e.message)
            sleep(5)

    call_command('syncdb')
    call_command('migrate')
    time.sleep(20)
    call_command('es_reindex_recipes')
