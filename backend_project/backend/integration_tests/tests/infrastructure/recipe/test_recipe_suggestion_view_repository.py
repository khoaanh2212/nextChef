from books.models import Book
from chefs.models import Chefs
from infrastructure.recipe.RecipeSuggestionViewRepository import RecipeSuggestionViewRepository
from integration_tests.integration_test_case import IntegrationTestCase
from recipe.models import Recipes
from test_data_provider.BookDataProvider import BookDataProvider
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.RecipeDataProvider import RecipeDataProvider


class RecipeSuggestionViewRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(RecipeSuggestionViewRepositoryTest, self).setUp()
        self.sut = RecipeSuggestionViewRepository.new()

    def test_find_by_chef_should_returnListOfRecipeAccessibleByChef(self):
        chef = ChefDataProvider.get().withEmail('a@mi.com').build()
        chef.save()
        instances = self.exercise_create_test_data(chef)
        actual = self.sut.find_by_chef(chef)
        actual = map(lambda x: x.recipe_name, actual)
        expected = ['recipe-1', 'recipe-2', 'recipe-3', 'recipe-4']
        self.assertEqual(actual, expected)
        self.delete_all(instances)

    def test_find_by_chef_should_returnListOfRecipeAccessibleByChef_whenFilter(self):
        chef = ChefDataProvider.get().withEmail('b@mi.com').build()
        chef.save()
        instances = self.exercise_create_test_data(chef)
        actual = self.sut.find_by_chef(chef, filter='1')
        actual = list(set(map(lambda x: x.recipe_name, actual)))
        expected = ['recipe-1']
        self.assertEqual(actual, expected)

        self.delete_all(instances)

    def exercise_create_test_data(self, chef):
        recipe1 = RecipeDataProvider.get().with_name('recipe-1').active().build()
        recipe2 = RecipeDataProvider.get().with_name('recipe-2').active().build()
        recipe3 = RecipeDataProvider.get().with_name('recipe-3').active().build()
        recipe4 = RecipeDataProvider.get().with_name('recipe-4').active().build()
        recipe5 = RecipeDataProvider.get().with_name('recipe-5').active().build()
        recipe6 = RecipeDataProvider.get().with_name('recipe-6').active().build()
        recipe7 = RecipeDataProvider.get().with_name('recipe-7').build()
        self.save_all([recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7])

        book1 = BookDataProvider.get().with_name('book-1').with_collaborators('[%d],' % chef.id) \
            .with_book_type('P').build()
        book2 = BookDataProvider.get().with_name('book-2').with_book_type('N').build()
        book3 = BookDataProvider.get().with_name('book-3').with_book_type('P').build()
        book4 = BookDataProvider.get().with_name('book-4').with_book_type('P').build()
        self.save_all([book1, book2, book3, book4])
        # collaborator case - show recipe-1, recipe-3
        book1.add_recipe(recipe1)
        book1.add_recipe(recipe3)
        book1.save()
        # public case - show recipe-2 (recipe-7 is draft, not showing)
        book2.add_recipe(recipe1)
        book2.add_recipe(recipe2)
        book2.add_recipe(recipe7)
        book2.save()
        # owner case - show recipe-4
        book3.chef = chef
        book3.add_recipe(recipe4)
        book3.save()
        # private case - not show
        book4.add_recipe(recipe5)
        book4.add_recipe(recipe6)
        book4.save()

        return {
            "recipes": [recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7],
            "books": [book1, book2, book3, book4],
            "chefs": [chef]
        }

    def save_all(self, instances):
        for ins in instances:
            ins.save()

    def delete_all(self, instance):
        Chefs.objects.filter(id__in=self.get_ids(instance["chefs"]))
        Recipes.objects.filter(id__in=self.get_ids(instance["recipes"]))
        Book.objects.filter(id__in=self.get_ids(instance["books"]))

    def get_ids(self, instances):
        return map(lambda x: x.id, instances)
