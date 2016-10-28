from books.models import Book
from integration_tests.api_test_case import ApiTestCase

from recipe.models import Recipes


class BooksTest(ApiTestCase):
    def create_recipe(self):
        url = '/0/recipes'
        data = {
            'commensals': 1,
            'private': 0,
            'draft': 0,
            'name': 'Recipe',
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        return resp.data['recipe']

    def test_get_books(self):
        """
        Test get books a recipe is in
        """
        self.create_recipe()
        recipe = Recipes.objects.last()

        url = '/0/recipes/%i/books' % recipe.pk

        book = Book.objects.create(name='Book 1', chef=self.user)
        book.add_recipe(recipe)

        user2 = self.create_user('2')
        book_other = Book.objects.create(name='Book 1', chef=user2)
        book_other.add_recipe(recipe)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('books', resp.data)
        books = resp.data['books']
        self.assertEqual(len(books), 1)
        keys = ('added', 'name', 'edit_date', 'nb_added', 'chef', 'nb_shares', 'nb_comments',
                'creation_date', 'id', 'book_type', 'status', 'price', 'product_id')
        self.assertEqual(set(books[0].keys()), set(keys))
