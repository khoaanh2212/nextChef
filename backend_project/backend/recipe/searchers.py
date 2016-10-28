from elasticutils import Q
from elasticutils.contrib.django import MappingType, Indexable

from .models import Recipes


class RecipeMapping(MappingType, Indexable):
    @classmethod
    def get_index(cls):
        return 'cookbooth-recipes'

    @classmethod
    def get_model(cls):
        return Recipes

    @classmethod
    def get_mapping_type_name(cls):
        return 'recipe'

    @classmethod
    def get_mapping(cls):
        return {
            'properties': {
                'name': {
                    'type': 'string',
                    'analyzer': 'standard'
                },
                'chefName': {
                    'type': 'string',
                    'analyzer': 'default'
                },
                'bookNames': {
                    'type': 'string',
                    'analyzer': 'standard'
                },
                'ingredientNames': {
                    'type': 'string',
                    'analyzer': 'standard'
                },
                'tagNames': {
                    'type': 'string',
                    'analyzer': 'standard'
                },
                'forSale': {
                    'type': 'boolean',
                    'analyzer': 'standard'
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
            'chefName': u"%s %s" % (obj.chef.name, obj.chef.surname.strip()),
            'bookNames': [book for book in obj.book_set.all().values_list('name').distinct()],
            'ingredientNames': [ingredient for ingredient in obj.ingredients.all().values_list('name').distinct()],
            'tagNames': [tag for tag in obj.tags.all().values_list('name').distinct()],
            'forSale': obj.is_in_book_for_sale,
        }

    @classmethod
    def cookbooth_search(cls, search_str, fields=None, hide_for_sale=False):
        search_str = search_str.lower() if search_str else ""

        fields = fields or []
        q = Q()

        if hide_for_sale:
            q += Q(forSale=False)

        if not fields or ('recipe' in fields and 'chef' in fields and
                          'book' in fields and 'ingredient' in fields):
            q += Q(name__query_string=search_str, should=True)
            q += Q(tagNames__query_string=search_str, should=True)
            q += Q(chefName__query_string=search_str, should=True)
            q += Q(bookNames__query_string=search_str, should=True)
            q += Q(ingredientNames__query_string=search_str, should=True)
        else:
            if 'recipe' in fields:
                q += Q(name__query_string=search_str, should=True)
                q += Q(tagNames__query_string=search_str, should=True)

            if 'chef' in fields:
                q += Q(chefName__query_string=search_str, should=True)

            if 'book' in fields:
                q += Q(bookNames__query_string=search_str, should=True)
                q += Q(tagNames__query_string=search_str, should=True)

            if 'ingredient' in fields:
                q += Q(ingredientNames__query_string=search_str, should=True)
                q += Q(tagNames__query_string=search_str, should=True)

        searcher = cls.search()
        searcher = searcher.boost(name=8.0, chefName=4.0, ingredientNames=6.0)
        qry = searcher.query(q)[:240]

        return qry

    @classmethod
    def cookbooth_search_list(cls, search_str, fields=None):
        """
        Elasticsearch with object models list
        :param search_str:
        :param fields:
        :return:
        """
        results = RecipeMapping.cookbooth_search(search_str, fields)
        obj_list = []
        for r in results:
            try:
                obj_list.append(r.get_object())
            except Recipes.DoesNotExist:
                pass
        return obj_list
