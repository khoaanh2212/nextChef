from books.models import Book
from infrastructure.book.BookRepository import BookRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.RecipeDataProvider import RecipeDataProvider


class BookRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(BookRepositoryTest, self).setUp()
        self.chef = ChefDataProvider.getDefault()
        self.chef.id = 9999
        self.chef.save()
        self.sut = BookRepository.new()
        self.test_material = self.exercise_create_book_with_recipes()

    def test_getBooksByCollaborator_should_returnExpected(self):
        actual = self.sut.getBooksByCollaborator(self.chef, 2)
        actual = map(lambda x: x.name, actual)
        expected = ['book-1']

        self.assertEqual(actual, expected)

    def test_get_recipe_by_chef_should_returnExpected(self):
        actual = self.sut.get_recipe_by_chef(self.chef)
        actual = map(lambda x: x.name, actual)
        expected = ['recipe-1', 'recipe-2', 'recipe-4', 'recipe-5']
        self.assertEqual(actual, expected)

    def test_get_book_by_chef_should_returnExpected(self):
        actual = self.sut.get_book_by_chef(self.chef)
        actual = map(lambda x: x.name, actual)
        expected = ['book-1', 'book-3']
        self.assertEqual(actual, expected)

    def test_get_recipe_by_books_should_return_all_recipes_in_books(self):
        actual = self.sut.get_recipe_by_books(self.test_material['books'])
        expected = self.test_material['recipes']
        self.assertEqual(actual, expected)

    def test_get_recipe_by_following_chef_should_return_all_recipe_public_of_chef_follow(self):
        actual = self.sut.get_recipe_by_following_chef(self.chef)
        actual = map(lambda x: x.name, actual)
        expected = ['recipe-5']
        self.assertEquals(actual, expected)

    def test_is_recipe_belong_to_public_book_should_returnTrue_whenRecipeBelongToPublicBook(self):
        recipe = self.test_material['recipes'][0]
        actual = self.sut.is_recipe_belong_to_public_book(recipe)
        self.assertTrue(actual)

    def test_is_recipe_belong_to_public_book_should_returnFalse_whenRecipeNotBelongToPublicBook(self):
        recipe = self.test_material['recipes'][3]
        actual = self.sut.is_recipe_belong_to_public_book(recipe)
        self.assertFalse(actual)

    def test_is_collaborator_of_recipe_should_returnTrue_whenChefIsCollaboratorOfABookContainsRecipe(self):
        recipe = self.test_material['recipes'][0]
        chef_id = 1
        actual = self.sut.is_collaborator_of_recipe(chef_id, recipe)
        self.assertTrue(actual)

    def test_is_collaborator_of_recipe_should_returnFalse_whenChefIsNotCollaboratorOfABookContainsRecipe(self):
        recipe = self.test_material['recipes'][0]
        chef_id = 4
        actual = self.sut.is_collaborator_of_recipe(chef_id, recipe)
        self.assertFalse(actual)

    def exercise_create_book_with_recipes(self):
        recipe1 = RecipeDataProvider.get().with_name('recipe-1').with_id(1).active().build()
        recipe2 = RecipeDataProvider.get().with_name('recipe-2').with_id(2).active().build()
        recipe3 = RecipeDataProvider.get().with_name('recipe-3').with_id(3).build()
        recipe4 = RecipeDataProvider.get().with_name('recipe-4').with_id(4).active().build()
        recipe5 = RecipeDataProvider.get().with_name('recipe-5').with_id(5).active().build()
        recipe6 = RecipeDataProvider.get().with_name('recipe-6').with_id(6).build()
        recipe7 = RecipeDataProvider.get().with_name('recipe-7').with_id(7).active().build()
        self.save([recipe1, recipe2, recipe3, recipe4, recipe5, recipe6, recipe7])

        book1 = self._saveBook('book-1', '[1],[2],[3]')
        book1.book_type = 'N'
        book1.private = False
        book2 = self._saveBook('book-2', '[2],[5],[6]')
        book3 = self._saveBook('book-3', '[3],[4],[5],[%d]' % self.chef.id)
        book4 = self._saveBook('book-4', '')
        chefFollow = ChefDataProvider.get().withEmail('chefFollow@cmail.com').withId(8888).build()
        chefFollow.save()
        self.chef.follow(chefFollow)

        book1.add_recipe(recipe1)
        book1.add_recipe(recipe2)
        book1.chef = self.chef
        book1.save()
        book2.add_recipe(recipe1)
        book2.add_recipe(recipe3)
        book2.add_recipe(recipe7)
        book2.save()
        book3.add_recipe(recipe4)
        book3.save()
        book4.add_recipe(recipe5)
        book4.add_recipe(recipe6)
        book4.private = False
        book4.book_type = 'N'
        book4.status = 'A'
        book4.chef = chefFollow
        book4.save()

        return dict(
            books=[book1, book2, book3, book4],
            recipes=[recipe1, recipe2, recipe1, recipe7, recipe4, recipe5]
        )

    def _saveBook(self, book_name, collaborators):
        book = Book(name=book_name, collaborators=collaborators)
        book.save()
        return book

    def save(self, instances):
        for ins in instances:
            ins.save()
