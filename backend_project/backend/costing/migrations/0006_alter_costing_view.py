# -*- coding: utf-8 -*-
import os
from south.v2 import DataMigration
from infrastructure.sql_file_runner import run_sql_file


class Migration(DataMigration):

    def forwards(self, orm):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, '0006_alter_costing_view.sql')
        run_sql_file(file_path)

    def backwards(self, orm):
        raise RuntimeError("Can't go backwards")

    complete_apps = ['costing']

