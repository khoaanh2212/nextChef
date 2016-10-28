import mock
import unittest

from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from domain.costing.generic_ingredient.GenericIngredientService import GenericIngredientService, InvalidGenericIngredientArgumentException
from test_data_provider.GenericIngredientDataProvider import GenericIngredientDataProvider


class GenericIngredientServiceTest(unittest.TestCase):

    def setUp(self):
        self.modelStub = mock.Mock()
        self.repositoryStub = mock.Mock()
        self.sut = GenericIngredientService.new(self.modelStub, self.repositoryStub)

    def test_getAll_should_forwardCorrectParams(self):
        self.sut.getAll('celery', 5)
        self.repositoryStub.findAll.assert_called_with(filter='celery', page=5)

    def test_getAll_should_returnResultFromRepository(self):
        self.repositoryStub.findAll.return_value = 'actual-result'
        actual = self.sut.getAll()
        self.assertEqual(actual, 'actual-result')

    def test_find_by_id_should_returnExpected(self):
        ingredient = GenericIngredientDataProvider.getDefault()
        self.repositoryStub.findById.return_value = ingredient
        actual = self.sut.get_by_id('1')
        self.assertEqual(actual, ingredient)

    def test_find_by_id_should_throw(self):
        self.repositoryStub.findById = mock.Mock(side_effect=GenericIngredient.DoesNotExist)
        self.assertRaises(InvalidGenericIngredientArgumentException, self.sut.get_by_id, 1)
