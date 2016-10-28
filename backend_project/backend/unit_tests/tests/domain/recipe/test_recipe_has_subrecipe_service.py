import mock, unittest
from domain.recipe.RecipeHasSubrecipeService import RecipeHasSubrecipeService
from test_data_provider.RecipeHasSubrecipeDataProvider import RecipeHasSubrecipe, RecipeHasSubrecipeDataProvider


class RecipeHasSubRecipeServiceTest(unittest.TestCase):
    def setUp(self):
        self.repositoryStub = mock.Mock();
        self.sut = RecipeHasSubrecipeService.new(self.repositoryStub)

    def test_getBigestOrder_should_return_zero_if_has_no_sub_recipe(self):
        self.repositoryStub.find_by_recipe_id.return_value = []
        actual = self.sut.getBigestOrder(1)
        self.assertEqual(actual, 0)

    def test_getBigestOrder_should_return_value_if_has_sub_recipe(self):
        recipeHasSubRecipe_1 = RecipeHasSubrecipeDataProvider.get().with_order(1).build()
        recipeHasSubRecipe_2 = RecipeHasSubrecipeDataProvider.get().with_order(2).build()
        self.repositoryStub.find_by_recipe_id.return_value = [recipeHasSubRecipe_1, recipeHasSubRecipe_2]
        actual = self.sut.getBigestOrder(1)
        self.assertEqual(actual, 2)
