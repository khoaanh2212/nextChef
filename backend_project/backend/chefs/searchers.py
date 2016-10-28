from elasticutils import Q
from elasticutils.contrib.django import MappingType, Indexable

from .models import Chefs

class ChefMapping(MappingType, Indexable):
    @classmethod
    def get_model(cls):
        return Chefs

    @classmethod
    def get_mapping_type_name(cls):
        return 'chef'

    @classmethod
    def get_mapping(cls):
        return {
            'properties': {
                'name': {
                    'type': 'string',
                },
                'surname': {
                    'type': 'string',
                },
                'nbLikes': {
                    'type': 'integer',
                },
                'nbFollowers': {
                    'type': 'integer',
                },
            }
        }

    @classmethod
    def extract_document(cls, obj_id, obj=None):
        if obj is None:
            obj = cls.get_model().get(pk=obj_id)

        return {
            'id': obj.pk,
            'name': obj.name,
            'surname': obj.surname,
            'nbLikes': obj.nb_likes,
            'nbFollowers': obj.nb_followers,
        }

    @classmethod
    def cookbooth_search(cls, search_str):
        search_str = '*%s*' % search_str
        q = Q(_all__query_string=search_str, should=True)
        searcher = cls.search()
        return searcher.query(q)
