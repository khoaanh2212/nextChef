# -*- coding: utf-8 -*-
import os
from south.v2 import DataMigration
from infrastructure.sql_file_runner import run_sql_file
from django.conf import settings


class Migration(DataMigration):
    depends_on = (
        ('application', '0003_books_add_field_private'),
    )

    def forwards(self, orm):
        module_dir = os.path.dirname(__file__)  # get current directory
        if settings.TESTING:
            file_path = os.path.join(module_dir, '0020_recipe_permission_view.sql')
        else:
            file_path = os.path.join(module_dir, '0020_recipe_permission_view_sqlite.sql')
        run_sql_file(file_path)

    def backwards(self, orm):
        raise RuntimeError("Can't go backwards")

    complete_apps = ['recipe']

