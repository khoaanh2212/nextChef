from chefs.models import Chefs
from domain.recipe.SelectedAllergens import SelectedAllergens
from infrastructure.recipe.RecipeRepository import RecipeRepository
from integration_tests.integration_test_case import IntegrationTestCase
from legacy_wrapper.recipe_wrapper import Recipe
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.RecipeDataProvider import RecipeDataProvider


class RecipeRepositoryTest(IntegrationTestCase):

    def setUp(self):
        super(RecipeRepositoryTest, self).setUp()
        self.chef = Chefs.objects.create_user('Test', 'Tests', 'testUpdateRecipe@example.com', 'secret')

    sut = RecipeRepository.new()

    def test_whenISaveAllergensInRecipe_theyCanBeFoundLater(self):
        expected = SelectedAllergens.new(["Celery"])
        recipe = Recipe.new(chef=self.chef, name="Recipe 1", draft=False)
        recipe.set_allergens(expected)
        self.sut.save(recipe)

        recipe = self.sut.findById(recipe.toDTO()['id'])
        actual = recipe.get_allergens()

        self.assertEquals(actual.toAllergenString(), expected.toAllergenString())

    def test_WhenGetAllPublicRecipeByName_ItShouldReturnExpected(self):
        user = Chefs.objects.create_user('Test', 'Tests', 'test@example.com', 'secret')
        self.sut.save(Recipe.new(chef=user, name='Recipe 1 keyword', draft=True, private=False))
        self.sut.save(Recipe.new(chef=user, name='Recipe 2 keyword', draft=False, private=False))
        self.sut.save(Recipe.new(chef=user, name='Recipe 3 keyword', draft=False, private=False))
        self.sut.save(Recipe.new(chef=user, name='Recipe 4 keyword', draft=False, private=True))

        expected = ['Recipe 2 keyword', 'Recipe 3 keyword']
        actual = map(lambda recipe: recipe.name, self.sut.get_all_public('keyword'))

        self.assertEquals(actual, expected)

    def test_updateAllergensOrIngredient_shouldDeleteOldOne(self):
        recipe = self.sut.save(Recipe.new(chef=self.chef, name='Recipe', draft=False, private=False))
        recipe_id = recipe.toDTO()['id']
        self.sut.update_allergens_or_ingredient(recipe_id, '', '')
        actual = Recipe.objects.filter(id=recipe_id)
        self.assertEqual(actual.__len__(), 0)

    def test_find_by_ids_for_explore_should_returnExpected(self):
        chef1 = ChefDataProvider.get().withEmail('chef1@email.com').withId(1).build()
        chef1.save()
        chef2 = ChefDataProvider.get().withEmail('chef2@email.com').withId(2).build()
        chef2.save()
        recipe1 = self.sut.save(RecipeDataProvider.get().active().with_chef(chef1).build())
        recipe2 = self.sut.save(RecipeDataProvider.get().active().with_chef(chef2).build())

        ids = [recipe1.id, recipe2.id]

        actual = self.sut.find_by_ids_for_explore(ids, chef1)
        actual = map(lambda x: x.id, actual)
        self.assertEqual(actual, [recipe2.id])
