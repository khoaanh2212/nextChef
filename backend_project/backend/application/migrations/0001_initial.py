# -*- coding: utf-8 -*-
import os
from south.db import db
from south.v2 import DataMigration
import logging
from infrastructure.sql_file_runner import run_sql_file

def system(command):
    logging.info(command)
    return os.system(command)

class Migration(DataMigration):
    initial = True
    depends_on = (
        ('banners', '0001_initial'),
        ('books', '0007_auto__add_field_book_image'),
        ('chefs', '0008_auto__add_subscriptionpayment__add_subscription__add_plan__add_stripep'),
        ('colls', '0002_auto__add_field_collection_description'),
        ('emailing', '0004_auto__add_field_emailinglist_page__add_field_emailinglist_page_size'),
        ('metrics', '0003_auto__chg_field_metric_created'),
        ('notifications', '0006_auto__add_field_notification_followed'),
        ('products', '0005_auto__add_field_product_barcode'),
        ('recipe', '0011_auto__add_field_recipes_explore_noted'),
        ('subscribers', '0001_initial'),
    )

    def forwards(self, orm):

        env_test_data = os.getenv('TEST_DATA', 'false')

        file_path = os.path.join(os.path.dirname(__file__), '0001_initial_test_data.sql')

        #dump = "nextchef-test-data.sql"

        if not env_test_data == 'true':
            logging.info("Skipping TEST DATA %s, as declared in configuration" % file_path)
            return

        if db.backend_name == 'sqlite3':
            logging.info("Skipping TEST DATA %s, because is not compatible with sqlite" % file_path)
            return


        #system("cp /dumps/%s.gz /tmp" % dump)
        #system("gunzip /tmp/%s.gz" % dump)

        #run_sql_file("/tmp/%s" % dump)
        run_sql_file(file_path)

        #logging.info("TEST DATA /dump/%s imported" % dump)


    def backwards(self, orm):
        raise RuntimeError("Can't go backwards")

    complete_apps = ['application']
