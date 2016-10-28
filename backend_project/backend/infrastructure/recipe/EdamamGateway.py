import json, os, logging, requests
from django.core.cache import get_cache
from django.conf import settings
from domain.recipe.SelectedAllergens import EdamamSelectedAllergens
from domain.recipe.ingredient.Ingredient import Ingredient


class EdamamPermissionException(Exception):
    pass

class EdamamServerException(Exception):
    pass

class InvalidEdamamArgumentException(Exception):
    pass


class EdamamGateway:

    def __init__(self, cache, logger, requests, edamamSelectedAllergens):
        self.cache = cache
        self.logger = logger
        self.requests = requests
        self.edamamSelectedAllergens = edamamSelectedAllergens

    def verify_ingredient(self, ingredient):

        key = 'NUTRITION_DATA_' + json.dumps(ingredient.text)

        if(self.cache.get(key)):
            response = json.loads(self.cache.get(key))
            self.logger.info('Retrieved ingredient information from CACHE')

        else:
            response = self._get_edamam_nutrition_data(ingredient.text)
            self.cache.set(key, json.dumps(response))
            self.logger.info('Retrieved ingredient information from SERVER')

        try:
            ingredient.measure = response['ingredients'][0]['parsed'][0]['measure']
            ingredient.quantity = response['ingredients'][0]['parsed'][0]['quantity']
            ingredient.weight_in_gr = response['ingredients'][0]['parsed'][0]['weight']
            ingredient.allergens = self._extractAllergenFromEdamam(response)
        except KeyError:
            raise InvalidEdamamArgumentException

        return ingredient

    def getAllergens(self, request):

        key = json.dumps(request)
        cached = False

        if(self.cache.get(key)):
            edamam_response = json.loads(self.cache.get(key))
            cached = True
            self.logger.info('Retrieved allergens from CACHE')

        else:
            edamam_response = self._getEdamamResponse(request)
            self.cache.set(key, json.dumps(edamam_response))
            self.logger.info('Request for allergens from SERVER')

        self.logger.debug(key)
        self.logger.debug(edamam_response)

        allergens = self._extractAllergenFromEdamam(edamam_response)
        
        return dict(
            allergens = allergens,
            response = edamam_response,
            cached = cached
        )

    def _extractAllergenFromEdamam(self, edamam_response):
        edamam_allergens_free = edamam_response['healthLabels']
        return self.edamamSelectedAllergens.new(edamam_allergens_free)

    def _getEdamamResponse(self, request):

        url = "%s?app_id=%s&app_key=%s" % (settings.EDAMAM_RECIPE_ANALYZE_API, settings.EDAMAM_APP_ID, settings.EDAMAM_APP_KEY)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.requests.post(url=url, data=json.dumps(request), headers=headers, timeout=10)

        self.logger.info('Requested to %s', url)
        self.logger.debug(request)
        self.logger.debug(response.status_code)

        if response.status_code == 200:
            result = response.json()

        elif response.status_code == 401:
            raise EdamamPermissionException

        else:
            raise EdamamServerException

        return result


    def _getFakeEdamamResponse(self, request):
        dir = os.path.dirname(os.path.realpath(__file__))
        json_data = open(dir + '/fake_edamam_response.json')
        return json.load(json_data)

    def _get_edamam_nutrition_data(self, ingredient_text):
        url = "%s?app_id=%s&app_key=%s&ingr=%s" % \
              (settings.EDAMAM_NUTRITION_API, settings.EDAMAM_APP_ID,
               settings.EDAMAM_NUTRITION_DATA_API_KEY, ingredient_text)

        response = self.requests.get(url)
        self.logger.info('Requested to %s', url)
        self.logger.debug(ingredient_text)
        self.logger.debug(response.status_code)

        if response.status_code == 200:
            result = response.json()

        elif response.status_code == 401:
            raise EdamamPermissionException

        else:
            raise EdamamServerException

        return result

    @staticmethod
    def new(cache = get_cache('default'),
            logger = logging.getLogger('EdamamGateway'),
            requests = requests,
            edamamSelectedAllergens = EdamamSelectedAllergens):
        return EdamamGateway(cache, logger, requests, edamamSelectedAllergens)
