# -*- coding: utf-8 -*-
import os
from south.v2 import DataMigration
from infrastructure.sql_file_runner import run_sql_file


class Migration(DataMigration):

    depends_on = (
        ('application', '0003_books_add_field_private'),
    )

    def forwards(self, orm):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, '0004_sub_recipe_suggestion_view.sql')
        run_sql_file(file_path)

    def backwards(self, orm):
        raise RuntimeError("Can't go backwards")

    complete_apps = ['application']

