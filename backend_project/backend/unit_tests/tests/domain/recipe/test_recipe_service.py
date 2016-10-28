import mock
import unittest
from domain.recipe.RecipeService import RecipeService
from test_data_provider.RecipeDataProvider import RecipeDataProvider
from legacy_wrapper.recipe_wrapper import Recipe
from test_data_provider.ChefDataProvider import ChefDataProvider


class RecipeServiceTest(unittest.TestCase):

    def setUp(self):
        self.repositoryStub = mock.Mock()
        self.recipe_suggestion_view_repository_stub = mock.Mock()
        self.sut = RecipeService.new(self.repositoryStub, self.recipe_suggestion_view_repository_stub)

    def test_getById_shouldCalledWithRepositoryMethod(self):
        spy = self.repositoryStub.findById = mock.Mock()
        self.sut.get_by_id(1)
        self.assertIsNone(spy.assert_called_with(1))

    def test_add_allergens_to_recipe_should_addAllergensToRecipe(self):
        self.repositoryStub.findById.return_value = Recipe(RecipeDataProvider.get().with_allergens("Fish, Celery").build())
        allergens = ['Peanuts', 'Fish', 'Milk']
        actual = self.sut.add_allergens_to_recipe('', allergens)
        self.assertTrue(self.repositoryStub.save.called)
        self.assertEqual(actual.allergens, "Celery, Peanuts, Fish, Milk")

    def test_remove_allergens_to_recipe_should_removeAllergensFromRecipe(self):
        self.repositoryStub.findById.return_value = Recipe(RecipeDataProvider.get().with_allergens("Fish, Celery").build())
        allergens = ['Fish']
        actual = self.sut.remove_allergens_from_recipe('', allergens)
        self.assertTrue(self.repositoryStub.save.called)
        self.assertEqual(actual.allergens, "Celery")

    def test_get_suggestion_list_should_returnExpected(self):
        chef = ChefDataProvider.getDefault()
        self.recipe_suggestion_view_repository_stub.find_by_chef.return_value = []
        actual = self.sut.get_suggestion_list(chef, '', 5)
        self.assertEqual(actual, [])

    def test_count_suggestion_list_should_returnExpected_whenHasNoMore(self):
        chef = ChefDataProvider.getDefault()
        self.recipe_suggestion_view_repository_stub.count_by_chef.return_value = 100
        actual = self.sut.count_suggestion_list(chef, '')
        self.assertEqual(actual, 100)

