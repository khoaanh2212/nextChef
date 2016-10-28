from domain.recipe.RecipeHasIngredient import RecipeHasIngredient
from infrastructure.recipe.RecipeHasIngredientRepository import RecipeHasIngredientRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.RecipeHasIngredientDataProvider import RecipeHasIngredientDataProvider


class RecipeHasIngredientRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(RecipeHasIngredientRepositoryTest, self).setUp()
        self.sut = RecipeHasIngredientRepository.new()
        RecipeHasIngredientDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasIngredientDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasIngredientDataProvider.get().with_recipe_id(1).with_price(100).build().save()
        RecipeHasIngredientDataProvider.get().with_recipe_id(2).with_price(100).build().save()
        RecipeHasIngredientDataProvider.get().with_recipe_id(3).with_price(100).build().save()

    def test_total_price_by_recipe_id_shouldGetTotalIngredientPrice(self):
        actual = self.sut.total_price_by_recipe_id(1)
        self.assertEqual(actual, 300)

    def test_total_price_by_recipe_id_shouldReturn0WhenNoIngredientAdded(self):
        actual = self.sut.total_price_by_recipe_id(4)
        self.assertEqual(actual, 0)

    def tearDown(self):
        RecipeHasIngredient.objects.filter(recipe_id__in=[1, 2, 3]).delete()
        super(RecipeHasIngredientRepositoryTest, self).tearDown()
