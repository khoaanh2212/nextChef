# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from recipe.searchers import RecipeMapping


class Command(BaseCommand):
    help = 'Create elasticsearch index for recipes.'

    def handle(self, *args, **options):
        settings = {
            'analysis': {
                'analyzer': {
                    'default': {
                        'tokenizer': 'standard',
                        'filter':  ['lowercase', 'asciifolding']
                    }
                }
            },
        }
        es = RecipeMapping.get_es()

        # Delete index if exists
        if es.indices.exists(RecipeMapping.get_index()):
            es.indices.delete(RecipeMapping.get_index())

        # Add our mapping configuration to the index settings
        settings.update(RecipeMapping.get_mapping())
        es.indices.create(RecipeMapping.get_index(), body=settings)

        self.stdout.write("Index for recipes created.")
