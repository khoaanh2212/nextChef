from books.models import Book, BookSale
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes


class BooksTest(ApiTestCase):
    def create_book(self):
        self.user2 = self.create_user('seller')
        data = {'name': "Book 1", 'chef': self.user2, 'book_type': Book.TO_SELL, 'price': 1.}
        book = Book.objects.create(**data)
        recipe = Recipes.objects.create(draft=False, private=False)
        book.add_recipe(recipe)
        return book

    def test_view_book(self):
        """
        Test view book
        """
        book = self.create_book()
        url = '/1/books/%i' % book.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('book', resp.data)
        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'video_app', 'video_web',
                'added', 'nb_added', 'nb_shares', 'nb_comments', 'price', 'product_id', 'book_type',
                'cover', 'recipes', 'description')
        self.assertEqual(set(keys), set(resp.data['book'].keys()))
        self.assertEqual(len(resp.data['book']['recipes']), 1)
        keys = set(('url', 'id', 'name', 'description'))
        self.assertEqual(set(resp.data['book']['recipes'][0].keys()), keys)

    def test_buy_book(self):
        """
        Test buy book
        """
        book = self.create_book()
        url = '/1/books/%i/buy' % book.pk

        data = {
            'vendor': BookSale.GOOGLE,
            'transaction': 'TRANSACTION',
        }

        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertEqual(BookSale.objects.all().count(), 1)
        sale = BookSale.objects.first()
        self.assertEqual(sale.chef, self.user)
        self.assertEqual(sale.price, book.price)
        self.assertEqual(sale.transaction_id, "%s-%s" % (data['vendor'], data['transaction']))

    def test_view_book_for_sale(self):
        """
        Test list of books for sale
        """
        book = self.create_book()
        url = '/1/books/for-sale'

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(len(resp.data['results']), 1)
        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'video_app', 'video_web',
                'price', 'book_type', 'cover', 'description', 'score', 'product_id', 'nb_added',
                'nb_shares', 'nb_comments', 'nb_recipes', 'url')

        self.assertEqual(set(keys), set(resp.data['results'][0].keys()))
