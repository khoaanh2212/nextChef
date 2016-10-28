from books.models import Book
from chefs.models import Chefs
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes


class APIV1ChefsTest(ApiTestCase):
    def test_get_onboard(self):
        """
        Test get on-board chefs
        """
        chef2 = self.create_user('2')
        chef3 = self.create_user('3')
        chef4 = self.create_user('4')

        chef3.onboard_score = 1
        chef3.save()
        chef4.onboard_score = 2
        chef4.save()

        url = '/1/chefs/onboard'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(2, len(resp.data['results']))
        self.assertEqual(chef4.pk, resp.data['results'][0]['id'])

    def test_get_by_type(self):
        """
        Test get chefs by type
        """
        self.user.type = Chefs.TYPE_FOODIE

        chef2 = self.create_user('2')
        chef2.type = Chefs.TYPE_PRO

        chef3 = self.create_user('3')
        chef3.type = Chefs.TYPE_BRAND

        for user in self.user, chef2, chef3:
            user.cache_recipes = 1  # Fake number of recipes
            user.save()

        url = '/1/chefs/by-type'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        for type_ in 'foodies', 'pros', 'brands':
            self.assertIn(type_, resp.data)
            self.assertEqual(1, len(resp.data[type_]))

    def test_get_followings_list(self):
        """
        Test get followings
        """
        url = '/1/chefs/list/followings'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

    def test_get_loves(self):
        """
        Test get loves
        """
        url = '/1/chefs/list/loves'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

    def test_get_chefs_list(self):
        """
        Test get chefs all
        """
        for i in range(0, 3):
            c = Chefs.objects.create(email="email%s@example.com" % i, cache_recipes=1)

        url = '/1/chefs/list/chefs'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(int(len(resp.data['results'])), 3)
        keys = ('type_class', 'avatar', 'full_name', 'cover', 'url', 'nb_loves', 'role',
                'id', 'nb_followers', 'location')
        self.assertEqual(set(keys), set(resp.data['results'][0].keys()))

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

    def test_get_books(self):
        """
        Test get books of a chef
        """
        book1 = Book.objects.create(chef=self.user)
        book2 = Book.objects.create(chef=self.user, book_type=Book.TO_SELL)

        url = '/1/chefs/%i/books' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('books', resp.data)
        self.assertEqual(2, len(resp.data['books']))
        keys = ('added', 'name', 'edit_date', 'chef', 'creation_date', 'id', 'nb_likes',
                'nb_recipes', 'book_type', 'status', 'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['books'][0].keys()))

    def test_get_recipes(self):
        """
        Test get recipes of a chef
        """
        r1 = Recipes.objects.create(chef=self.user, name="Recipe 1", draft=True)
        r2 = Recipes.objects.create(chef=self.user, name="Recipe 2", draft=False)
        r3 = Recipes.objects.create(chef=self.user, name="Recipe 3", draft=False)
        book = Book.objects.create(chef=self.user, book_type=Book.TO_SELL)
        book.add_recipe(r3)

        url = '/1/chefs/%i/recipes' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(2, len(resp.data['results']))
        keys = ("liked", "public_url", "edit_date", "ingredients", "shared", "tags", "commented",
                "private", "id", "chef", "reported", "nb_shares", "added", "nb_added",
                "nb_comments", "draft", "commensals", "creation_date", "nb_likes", "name",
                "products", "prep_time", "serves", "bought", "book_for_sale", "description")
        self.assertEqual(set(keys), set(resp.data['results'][0].keys()))
        self.assertNotEqual(r1.pk, resp.data['results'][0]['id'])
        self.assertNotEqual(r1.pk, resp.data['results'][1]['id'])
