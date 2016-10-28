import mock
import unittest

from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from domain.costing.custom_changes_ingredient.CustomChangesIngredientService import CustomChangesIngredientService
from test_data_provider.CustomChangesIngredientDataProvider import CustomChangesIngredientDataProvider
from test_data_provider.ChefDataProvider import ChefDataProvider


class GenericIngredientServiceTest(unittest.TestCase):

    def setUp(self):
        self.modelStub = mock.Mock()
        self.repositoryStub = mock.Mock()
        self.sut = CustomChangesIngredientService.new(self.modelStub, self.repositoryStub)

    def test_update_custom_ingredient_should_forwardCorrectParams(self):
        ingredient = CustomChangesIngredientDataProvider.get_default()
        self.modelStub.create.return_value = ingredient
        ingredient.id = 1
        self.sut.update_custom_ingredient(1, '', '')
        self.repositoryStub.save.assert_called_with(ingredient)
