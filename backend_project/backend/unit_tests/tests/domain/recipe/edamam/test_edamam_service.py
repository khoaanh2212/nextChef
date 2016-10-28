import unittest, mock
from domain.recipe.edamam.EdamamService import EdamamService
from domain.recipe.edamam.Edamam import Edamam


class EdamamServiceTest(unittest.TestCase):

    def setUp(self):
        self.repository = mock.Mock()
        self.model = mock.Mock()
        self.edamam_gateway = mock.Mock()
        self.sut = EdamamService.new(
            repository=self.repository,
            model=self.model,
            edamam_gateway=self.edamam_gateway
        )
        self.ingredients = ['carrot', 'milk']
        self.edamam_gateway.getAllergens.return_value = dict(
            allergens = 'allergens',
            response = 'response',
            cached = False,
        )
        self.edamam = Edamam()
        self.model.create.return_value = self.edamam

    def test__decorateIngredients_should_returnJSONString(self):
        actual = self.sut._decorateIngredients(self.ingredients)
        expected = {"ingr": ["carrot", "milk"]}
        self.assertEqual(actual, expected)

    def test_getAllergens_should_returnEdamamGatewayAllergens(self):
        actual = self.sut.getAllergens(self.ingredients)
        self.assertEqual(actual, 'allergens')

    def test_getAllergens_should_saveAllergensRequestAndResponse_ifNotCached(self):
        self.sut.getAllergens(self.ingredients)
        self.repository.save.assert_called_with(self.edamam)

    def test_getAllergens_shouldNot_saveAllergensRequestAndResponse_ifCached(self):
        self.edamam_gateway.getAllergens.return_value = dict(
            allergens = 'allergens',
            response = 'response',
            cached = True,
        )
        self.sut.getAllergens(self.ingredients)
        self.assertFalse(self.repository.save.called)

    def test_verify_ingredient_should_returnResponseFromEdamamGateway(self):
        self.edamam_gateway.verify_ingredient.return_value = 'ingredient'
        actual = self.sut.verify_ingredient('')
        self.assertEqual(actual, 'ingredient')
