from django.utils.crypto import get_random_string

from books.models import Book
from chefs.models import Chefs
from infrastructure.recipe.RecipePermissionViewRepository import RecipePermissionViewRepository
from integration_tests.integration_test_case import IntegrationTestCase
from recipe.models import Recipes
from test_data_provider.BookDataProvider import BookDataProvider
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.RecipeDataProvider import RecipeDataProvider


class RecipePermissionViewRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(RecipePermissionViewRepositoryTest, self).setUp()
        self.sut = RecipePermissionViewRepository.new()
        self.instances = self.exercise_create_test_data()

    def test_find_public_recipe_should_returnListOfPublicRecipes(self):
        actual = self.sut.find_public_recipe()
        actual = map(lambda x: x.recipe_id, actual)
        expected = [self.instances['recipes'][1].id]
        self.assertEqual(actual, expected)

    def test_is_recipe_available_for_chef_should_returnTrueForChef2Recipe4(self):
        recipe_id = self.instances['recipes'][3].id
        chef_id = self.instances['chefs'][1].id
        actual = self.sut.is_recipe_available_for_chef(recipe_id, chef_id)
        self.assertTrue(actual)

    def test_is_recipe_available_for_chef_should_returnTrueForChef3Recipe2(self):
        recipe_id = self.instances['recipes'][1].id
        chef_id = self.instances['chefs'][2].id
        actual = self.sut.is_recipe_available_for_chef(recipe_id, chef_id)
        self.assertTrue(actual)

    def test_is_recipe_available_for_chef_should_returnFalseForChef3Recipe1(self):
        recipe_id = self.instances['recipes'][0].id
        chef_id = self.instances['chefs'][2].id
        actual = self.sut.is_recipe_available_for_chef(recipe_id, chef_id)
        self.assertFalse(actual)

    def test_find_visible_recipes_should_returnExpected(self):
        current_user_id = self.instances['chefs'][0].id
        homepage_user_id = self.instances['chefs'][1].id
        actual = self.sut.find_visible_recipes(current_user_id, homepage_user_id)
        actual = map(lambda x: x.recipe_id, list(actual))

        recipes = self.instances['recipes']
        self.assertEqual(actual, [recipes[0].id, recipes[3].id])

    def tearDown(self):
        self.delete_all(self.instances)
        super(RecipePermissionViewRepositoryTest, self).tearDown()

    def exercise_create_test_data(self):
        chef1 = ChefDataProvider.get().withEmail(get_random_string(length=32) + '@mi.com').build()
        chef1.save()

        chef2 = ChefDataProvider.get().withEmail(get_random_string(length=32) + '@mi.com').build()
        chef2.save()

        chef3 = ChefDataProvider.get().withEmail(get_random_string(length=32) + '@mi.com').build()
        chef3.save()

        recipe1 = RecipeDataProvider.get().with_chef(chef1).with_name('public-r-private-b').active().publish().build()
        recipe2 = RecipeDataProvider.get().with_chef(chef1).with_name('public-r-public-b').active().publish().build()
        recipe3 = RecipeDataProvider.get().with_chef(chef1).with_name('private-r-public-b').active().build()
        recipe4 = RecipeDataProvider.get().with_chef(chef1).with_name('private-r-private-b').active().build()
        self.save_all([recipe1, recipe2, recipe3, recipe4])

        book1 = BookDataProvider.get().with_chef(chef1).with_name('public').publish().build()
        book2 = BookDataProvider.get().with_chef(chef1) \
            .with_collaborators('[%d],' % chef2.id) \
            .with_name('private').build()
        self.save_all([book1, book2])

        book1.add_recipe(recipe2)
        book1.add_recipe(recipe3)
        book1.save()

        book2.add_recipe(recipe1)
        book2.add_recipe(recipe4)
        book2.save()

        return {
            "recipes": [recipe1, recipe2, recipe3, recipe4],
            "books": [book1, book2],
            "chefs": [chef1, chef2, chef3]
        }

    def save_all(self, instances):
        for ins in instances:
            ins.save()

    def delete_all(self, instance):
        Chefs.objects.filter(id__in=self.get_ids(instance["chefs"])).delete()
        Recipes.objects.filter(id__in=self.get_ids(instance["recipes"])).delete()
        Book.objects.filter(id__in=self.get_ids(instance["books"])).delete()

    def get_ids(self, instances):
        return map(lambda x: x.id, instances)
