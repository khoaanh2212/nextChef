import mock, unittest
from domain.recipe.RecipeHasIngredientService import RecipeHasIngredientService
from domain.recipe.RecipeHasIngredient import RecipeHasIngredient
from test_data_provider.RecipeHasIngredientDataProvider import RecipeHasIngredientDataProvider


class RecipeHasIngredientServiceTest(unittest.TestCase):
    def setUp(self):
        self.modelStub = mock.Mock()
        self.repositoryStub = mock.Mock()
        self.sut = RecipeHasIngredientService.new(self.modelStub, self.repositoryStub)

    def test_getBigestOrder_should_return_zero_if_has_no_ingredient(self):
        self.repositoryStub.find_by_recipe_id.return_value = []
        actual = self.sut.getBigestOrder(1)
        self.assertEqual(actual, 0)

    def test_getBigestOrder_should_return_value_if_has_ingredient(self):
        recipeHasIngredient_1 = RecipeHasIngredientDataProvider.get().with_order(1).build()
        recipeHasIngredient_2 = RecipeHasIngredientDataProvider.get().with_order(2).build()
        self.repositoryStub.find_by_recipe_id.return_value = [recipeHasIngredient_1, recipeHasIngredient_2]
        actual = self.sut.getBigestOrder(1)
        self.assertEqual(actual, 2)