import mock
import unittest
from domain.costing.CostingIngredientService import CostingIngredientService
from test_data_provider.ChefDataProvider import ChefDataProvider


class CostingIngredientServiceTest(unittest.TestCase):

    def setUp(self):
        self.repositoryStub = mock.Mock()
        self.sut = CostingIngredientService.new(self.repositoryStub)

    def test_getByRecipeId_shouldCallWithRepositoryMethod(self):
        spy = self.repositoryStub.find_by_chef_id = mock.Mock(chef_id='chef_id')
        self.sut.get_by_recipe_id(1)
        self.assertIsNone(spy.assert_called_with(chef_id=1))

    def test_get_costing_table_shouldCallWithRepositoryMethod(self):
        chef = ChefDataProvider.getDefault()
        self.repositoryStub.find_by_chef_id.return_value = 'result'
        actual = self.sut.get_costing_table(chef, 'filter', 2)
        self.repositoryStub.find_by_chef_id.assert_called_with(chef_id=chef.id, filter='filter', page=2)
        self.assertEqual(actual, 'result')

    def test_get_suggestion_list_should_returnExpected(self):
        chef = ChefDataProvider.getDefault()
        self.repositoryStub.find_by_chef_id.return_value = []
        actual = self.sut.get_suggestion_list(chef, '', 5)
        self.assertEqual(actual, [])

    def test_count_suggestion_list_should_returnExpected(self):
        chef = ChefDataProvider.getDefault()
        self.repositoryStub.count_by_chef_id.return_value = 100
        actual = self.sut.count_suggestion_list(chef, '')
        self.assertEqual(actual, 100)
