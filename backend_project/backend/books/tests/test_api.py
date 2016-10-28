from books.models import Book, BookHasRecipes
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes, Photos


class BooksTest(ApiTestCase):

    def create_book(self):
        url = '/0/books'
        data = {'name': 'Book 1'}
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        return resp.data['book']

    def test_create_book(self):
        """
        Test create book
        """
        url = '/0/books'

        data = {'name': 'Book 1'}
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('book', resp.data)
        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'added', 'nb_added',
                'nb_shares', 'nb_comments', 'book_type', 'status', 'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['book'].keys()))

    def test_update_book(self):
        """
        Test update book
        """
        book = self.create_book()
        url = '/0/books/%i' % book['id']

        data = {'name': 'New Book Name'}

        resp = self.client.put(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('book', resp.data)
        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'added', 'nb_added',
                'nb_shares', 'nb_comments', 'book_type', 'status', 'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['book'].keys()))
        self.assertEqual(Book.objects.last().name, data['name'])

    def test_delete_book(self):
        """
        Test delete book
        """
        book = self.create_book()
        url = '/0/books/%i' % book['id']

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertFalse(Book.objects.exists())

    def test_view_book(self):
        """
        Test view book
        """
        book = self.create_book()
        url = '/0/books/%i' % book['id']

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('book', resp.data)
        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'added', 'nb_added',
                'nb_shares', 'nb_comments', 'nb_likes', 'nb_recipes', 'book_type', 'status',
                'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['book'].keys()))

    def test_copy_book(self):
        """
        Test copy book
        """
        user2 = self.create_user('2')
        book = self.create_book()
        book = Book.objects.get(pk=book['id'])
        book.chef = user2
        book.save()

        url = '/0/books/%i' % book.pk
        resp = self.client.generic('copy', url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.generic('copy', url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('book', resp.data)

        keys = ('id', 'creation_date', 'edit_date', 'name', 'chef', 'added', 'book_type', 'status',
                'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['book'].keys()))

        keys = 'id', 'type', 'email', 'name', 'surname'
        self.assertEqual(set(keys), set(resp.data['book']['chef'].keys()))

        # Do not fail if trying to copy it again
        resp = self.client.generic('copy', url, **headers)
        self.assertEqual(resp.status_code, 200)

    def test_copy_own_book(self):
        """
        Test copy own book
        """
        book = self.create_book()
        url = '/0/books/%i' % book['id']

        headers = self.login()
        resp = self.client.generic('copy', url, **headers)
        self.assertEqual(resp.status_code, 400)


class BooksRecipesTest(ApiTestCase):
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

    def create_book(self):
        url = '/0/books'
        data = {'name': 'Book 1'}
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        return resp.data['book']

    def test_add_recipe_to_book(self):
        """
        Test add recipe to book
        """
        self.create_book()
        book = Book.objects.last()

        url = '/0/books/%i/recipes' % book.pk

        recipe = self.create_recipe()
        recipe = Recipes.objects.last()

        data = {'recipe': recipe.pk}

        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_delete_recipe_from_book(self):
        """
        Test delete recipe from book
        """
        self.create_book()
        book = Book.objects.last()

        url = '/0/books/%i/recipes' % book.pk

        recipe = self.create_recipe()
        recipe = Recipes.objects.last()

        # Add recipe
        data = {'recipe': recipe.pk}
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)

        # Delete recipe
        url += '/%i' % recipe.pk

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_show_recipes_from_book(self):
        """
        Test show recipes from book
        """
        self.create_book()
        book = Book.objects.last()

        url = '/0/books/%i/recipes' % book.pk

        recipe = self.create_recipe()
        recipe = Recipes.objects.last()

        # Add recipe
        data = {'recipe': recipe.pk}
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)

        # Show recipes
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('recipes', resp.data)
        self.assertEqual(1, len(resp.data['recipes']))

        keys = ("liked", "public_url", "edit_date", "ingredients", "shared", "tags", "commented",
                "private", "id", "chef", "reported", "nb_shares", "added", "nb_added",
                "nb_comments", "draft", "commensals", "creation_date", "nb_likes", "name",
                "products", "prep_time", "serves", "bought", "book_for_sale", "description")
        self.assertEqual(set(keys), set(resp.data['recipes'][0].keys()))


class BooksPhotosTest(ApiTestCase):
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

    def create_book(self):
        url = '/0/books'
        data = {'name': 'Book 1'}
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        return resp.data['book']

    def test_get_book_photos(self):
        """
        Test get book's photos
        """
        user2 = self.create_user('2')
        self.create_book()
        book = Book.objects.last()

        url = '/0/books/%i/photos' % book.pk

        recipe1 = self.create_recipe()
        recipe2 = self.create_recipe()
        recipe3 = self.create_recipe()
        recipe4 = self.create_recipe()

        recipe1 = Recipes.objects.get(pk=recipe1['id'])
        recipe2 = Recipes.objects.get(pk=recipe2['id'])
        recipe3 = Recipes.objects.get(pk=recipe3['id'])
        recipe4 = Recipes.objects.get(pk=recipe4['id'])

        recipe2.chef = user2
        recipe2.private = False
        recipe2.draft = False
        recipe2.save()

        recipe3.chef = user2
        recipe3.private = True
        recipe3.draft = False
        recipe3.save()

        recipe4.chef = user2
        recipe4.private = False
        recipe4.draft = True
        recipe4.save()

        Photos.objects.create(recipe=recipe1, photo_order=1)
        Photos.objects.create(recipe=recipe2, photo_order=1)
        Photos.objects.create(recipe=recipe3, photo_order=1)
        Photos.objects.create(recipe=recipe4, photo_order=1)

        BookHasRecipes.objects.create(book=book, recipe=recipe1)
        BookHasRecipes.objects.create(book=book, recipe=recipe2)
        BookHasRecipes.objects.create(book=book, recipe=recipe3)
        BookHasRecipes.objects.create(book=book, recipe=recipe4)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photos', resp.data)
        self.assertEqual(2, len(resp.data['photos']))
        keys = set(('id', 'url', 'creation_date', 'edit_date', 'instructions', 'time',
                    'temperature', 'quantity', 'recipe', 'cover', 'order'))
        self.assertEqual(keys, set(resp.data['photos'][0]))
