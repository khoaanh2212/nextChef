import unittest, mock, json
from infrastructure.recipe.EdamamGateway import EdamamGateway, EdamamServerException, EdamamPermissionException
from domain.recipe.SelectedAllergens import EdamamSelectedAllergens
from domain.recipe.ingredient.Ingredient import Ingredient


class EdamamGatewayTest(unittest.TestCase):
    def setUp(self):
        self.logger = mock.Mock()
        self.cache = mock.Mock()
        self.requests = mock.Mock()
        self.edamamSelectedAllergens = mock.Mock()
        self.sut = EdamamGateway.new(
            cache=self.cache,
            logger=self.logger,
            requests=self.requests,
            edamamSelectedAllergens=self.edamamSelectedAllergens,
        )
        self.edamam_json = '{' \
                           '"healthLabels": ["MILK_FREE", "SOY_FREE", "FISH_FREE"], ' \
                           '"ingredients": [ {"parsed": [ { "measure": "large", "quantity": 1, "weight": 125 } ]} ]' \
                           '}'

    def test_getAllergens_should_getAllergensFromServerIfNoCache(self):
        self.cache.get.return_value = None

        edamam_response = json.loads('{"healthLabels": "cereals, milk, fish"}')
        self.sut._getEdamamResponse = mock.MagicMock()
        self.sut._getEdamamResponse.return_value = edamam_response

        self.edamamSelectedAllergens.new.return_value = 'filtered-allergens'

        expected = dict(
            response=edamam_response,
            allergens='filtered-allergens',
            cached = False
        )

        actual = self.sut.getAllergens('')
        self.assertEqual(actual, expected)
        self.logger.info.assert_called_with('Request for allergens from SERVER')

    def test_getAllergens_should_getAllergensFromCacheIfCached_and_log(self):
        edamam_json = '{"healthLabels": "cached, values"}'
        self.cache.get.return_value = edamam_json
        self.sut._extractAllergenFromEdamam = mock.Mock()

        self.sut.getAllergens('')
        self.sut._extractAllergenFromEdamam.assert_called_with(json.loads(edamam_json))
        self.logger.info.assert_called_with('Retrieved allergens from CACHE')


    def test__extractAllergenFromEdamam_should_returnEdamamSelectedAllergensObject(self):
        edamam_response = json.loads('{"healthLabels": "cereals, milk, fish"}')
        edamam_selected_allergens = EdamamSelectedAllergens.new()
        self.edamamSelectedAllergens.new.return_value = edamam_selected_allergens
        actual = self.sut._extractAllergenFromEdamam(edamam_response)
        self.assertEqual(actual, edamam_selected_allergens)

    def test__getEdamamResponse_should_returnExpectedData(self):
        request = mock.Mock()
        request.status_code = 200
        request.json.return_value = 'post-result'
        self.requests.post.return_value = request

        actual = self.sut._getEdamamResponse('')
        self.assertEqual(actual, 'post-result')

    def test__getEdamamResponse_should_raiseEdamamPermissionException_ifServerReturn401(self):
        request = mock.Mock()
        request.status_code = 401
        self.requests.post.return_value = request
        self.assertRaises(EdamamPermissionException, self.sut._getEdamamResponse, '')

    def test__getEdamamResponse_should_raiseEdamamPermissionException_ifServerReturnOtherError(self):
        request = mock.Mock()
        request.status_code = 500
        self.requests.post.return_value = request
        self.assertRaises(EdamamServerException, self.sut._getEdamamResponse, '')

    def test__get_edamam_nutrition_data_should_returnExpectedData(self):
        request = mock.Mock()
        request.status_code = 200
        request.json.return_value = 'get-result'
        self.requests.get.return_value = request

        actual = self.sut._get_edamam_nutrition_data('')
        self.assertEqual(actual, 'get-result')

    def test__get_edamam_nutrition_data_should_raiseEdamamPermissionException_ifServerReturn401(self):
        request = mock.Mock()
        request.status_code = 401
        self.requests.get.return_value = request
        self.assertRaises(EdamamPermissionException, self.sut._get_edamam_nutrition_data, '')

    def test__get_edamam_nutrition_data_should_raiseEdamamPermissionException_ifServerReturnOtherError(self):
        request = mock.Mock()
        request.status_code = 500
        self.requests.get.return_value = request
        self.assertRaises(EdamamServerException, self.sut._get_edamam_nutrition_data, '')

    def test_verify_ingredient_should_verifyIngredientFromServerIfNoCache(self):
        self.cache.get.return_value = None
        ingredient = Ingredient('')

        edamam_response = json.loads(self.edamam_json)
        self.sut._get_edamam_nutrition_data = mock.MagicMock()
        self.sut._get_edamam_nutrition_data.return_value = edamam_response

        actual = self.sut.verify_ingredient(ingredient)

        self.assertTrue(isinstance(actual, Ingredient))

        self.logger.info.assert_called_with('Retrieved ingredient information from SERVER')

    def test_verify_ingredient_should_verifyIngredientFromCacheIfCached_and_log(self):

        self.cache.get.return_value = self.edamam_json
        self.sut._get_edamam_nutrition_data = mock.Mock()

        self.sut.verify_ingredient(Ingredient(''))
        self.logger.info.assert_called_with('Retrieved ingredient information from CACHE')
