from domain.recipe.RecipeHasSubrecipe import RecipeHasSubrecipe
from domain.recipe.SelectedAllergens import SelectedAllergens
from infrastructure.recipe.RecipeHasSubrecipeRepository import RecipeHasSubrecipeRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.RecipeDataProvider import RecipeDataProvider
from test_data_provider.RecipeHasSubrecipeDataProvider import RecipeHasSubrecipeDataProvider


class RecipeSubrecipeRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(RecipeSubrecipeRepositoryTest, self).setUp()
        self.sut = RecipeHasSubrecipeRepository.new()
        self.recipe1 = RecipeDataProvider.get().with_id(1).build()
        self.recipe2 = RecipeDataProvider.get().with_id(2).with_allergens('allergens').build()
        self.recipe2.chef = ChefDataProvider.getDefault()
        self.order = 1

        RecipeHasSubrecipeDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasSubrecipeDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasSubrecipeDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasSubrecipeDataProvider.get().with_recipe_id(2).with_price(100).build().save()
        RecipeHasSubrecipeDataProvider.get().with_recipe_id(3).with_price(100).build().save()

    def test_delete_shouldDeleteByRecipeId(self):
        recipe = RecipeHasSubrecipe.create(self.recipe1, self.recipe2, 50, SelectedAllergens([]), self.order, '')
        self.assertIsNone(self.sut.delete_by_recipe_id(recipe.r_id))

    def test_total_price_by_recipe_id_shouldGetTotalIngredientPrice(self):
        actual = self.sut.total_price_by_recipe_id(1)
        self.assertEqual(actual, 300)

    def test_total_price_by_recipe_id_shouldReturn0WhenNoIngredientAdded(self):
        actual = self.sut.total_price_by_recipe_id(4)
        self.assertEqual(actual, 0)
