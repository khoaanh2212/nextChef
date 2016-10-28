from mock import patch

from books.models import Book
from chefs.models import Chefs
from integration_tests.api_test_case import ApiTestCase, SENDY_PATH
from recipe.models import Recipes, Photos
from test_api import FACEBOOK_PATH, FACEBOOK_CONNECTIONS_PATH, IMAGES


class ChefsTest(ApiTestCase):
    CHEF_KEYS = set((
        'username', 'surname', 'name', 'language', 'languages', 'nb_followers', 'nb_likes',
        'nb_followings', 'email', 'edit_date', 'nb_books', 'nb_recipes', 'creation_date',
        'type', 'id', 'offline', 'private_recipes', 'cover'))
    CHEF_VIEW_KEYS = set((
        'username', 'interests', 'surname', 'name', 'language', 'languages', 'nb_followers',
        'nb_likes', 'nb_followings', 'email', 'edit_date', 'referents', 'nb_books', 'short_bio',
        'location', 'nb_recipes', 'creation_date', 'type', 'id', 'country', 'offline',
        'private_recipes', 'followed', 'cover'))

    @patch(SENDY_PATH)
    def test_signup(self, mocked_sendy):
        """
        Test registration
        """
        url = '/0/chefs'
        data = {
            'email': 'johndoe@example.com',
            'password': 'secret',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])

        # Test that we can log in
        url = '/0/chefs/login'
        data = {
            'email': 'johndoe@example.com',
            'password': 'secret',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_signup_existing_email(self):
        """
        Test fail when trying to signup with an existing email
        """
        url = '/0/chefs'
        data = {
            'email': self.user.email,
            'password': 'secret',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['code'], 400)
        self.assertEqual(resp.data['message'], 'Invalid parameters')
        self.assertIn('raw', resp.data)
        self.assertEqual(len(resp.data['raw']), 1)
        self.assertEqual(resp.data['raw'][0]['field'], 'email')
        self.assertIn('message', resp.data['raw'][0])

    def test_signup_invalid_params(self):
        """
        Test fail when sending invalid params at signup
        """
        url = '/0/chefs'

        # No data
        data = {}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['code'], 400)
        self.assertEqual(resp.data['message'], 'Invalid parameters')
        self.assertIn('raw', resp.data)
        error_keys = [e['field'] for e in resp.data['raw'] if 'field' in e]
        self.assertEqual(set(['email', 'name', 'language']), set(error_keys))

        # Everything but password or fb_access_token
        data = {
            'email': 'johndoe@example.com',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['code'], 400)
        self.assertEqual(resp.data['message'], 'Invalid parameters')
        self.assertEqual(len(resp.data['raw']), 1)

    def test_update_self(self):
        """
        Test self modification
        """
        # Test that we can log in
        url = '/0/chefs/login'
        data = {
            'email': self.user.email,
            'password': self.user.password,
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

        # Test update
        url = '/0/chefs/' + str(self.user.pk)
        # Although don't change anything
        data = {}
        resp = self.client.put(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.CHEF_KEYS, set(resp.data['chef'].keys()))

        # Test that we can still log in
        url = '/0/chefs/login'
        data = {
            'email': self.user.email,
            'password': self.user.password,
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

    def test_update_self_fail(self):
        """
        Test self modification fail
        """
        new_user = self.create_user('1')
        url = '/0/chefs/' + str(new_user.pk)

        headers = self.login()
        resp = self.client.put(url, **headers)
        self.assertInvalidCredentials(resp)

    def test_get_self(self):
        """
        Test get self Chef
        """
        url = '/0/chefs'

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('chef', resp.data)
        self.assertEqual(self.CHEF_VIEW_KEYS - set(['followed']), set(resp.data['chef'].keys()))

    def test_get_chef(self):
        """
        Test get Chef
        """
        url = '/0/chefs/' + str(self.user.pk)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('chef', resp.data)
        self.assertEqual(self.CHEF_VIEW_KEYS, set(resp.data['chef'].keys()))

    def test_get_chef_with_photo(self):
        """
        Test get Chef with photo
        """
        url = '/0/chefs/' + str(self.user.pk)
        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('chef', resp.data)
        self.assertNotIn('photo', resp.data['chef'])

        self.user.avatar_photos.create(s3_url='image')  # Create photo
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('chef', resp.data)
        self.assertIn('photo', resp.data['chef'])
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['chef']['photo']))

    def test_delete(self):
        """
        Test delete account
        """
        url = '/0/chefs/' + str(self.user.pk)

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_chef_languages(self):
        """
        Test chef languages
        """
        url = '/0/chefs/' + str(self.user.pk)
        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([], resp.data['chef']['languages'])

        data = {'languages': 'en es'}
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(set(['en', 'es']), set(resp.data['chef']['languages']))

    def test_get_drafts(self):
        """
        Test get drafts of a chef
        """
        r1 = Recipes.objects.create(chef=self.user, name="Recipe 1", draft=True)
        r2 = Recipes.objects.create(chef=self.user, name="Recipe 2", draft=False)

        url = '/0/chefs/%i/drafts' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('drafts', resp.data)
        self.assertEqual(1, len(resp.data['drafts']))
        keys = ("liked", "public_url", "edit_date", "ingredients", "shared", "tags", "commented",
                "private", "id", "chef", "reported", "nb_shares", "added", "nb_added",
                "nb_comments", "draft", "commensals", "creation_date", "nb_likes", "name",
                "products", "prep_time", "serves", "bought", "book_for_sale", "description")
        self.assertEqual(set(keys), set(resp.data['drafts'][0].keys()))
        self.assertEqual(r1.pk, resp.data['drafts'][0]['id'])

    def test_get_recipes(self):
        """
        Test get recipes of a chef
        """
        r1 = Recipes.objects.create(chef=self.user, name="Recipe 1", draft=True)
        r2 = Recipes.objects.create(chef=self.user, name="Recipe 2", draft=False)
        r3 = Recipes.objects.create(chef=self.user, name="Recipe 3", draft=False)
        book = Book.objects.create(chef=self.user, book_type=Book.TO_SELL)
        book.add_recipe(r3)

        url = '/0/chefs/%i/recipes' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipes', resp.data)
        self.assertEqual(1, len(resp.data['recipes']))
        keys = ("liked", "public_url", "edit_date", "ingredients", "shared", "tags", "commented",
                "private", "id", "chef", "reported", "nb_shares", "added", "nb_added",
                "nb_comments", "draft", "commensals", "creation_date", "nb_likes", "name",
                "products", "prep_time", "serves", "bought", "book_for_sale", "description")
        self.assertEqual(set(keys), set(resp.data['recipes'][0].keys()))
        self.assertEqual(r2.pk, resp.data['recipes'][0]['id'])

    def test_get_books(self):
        """
        Test get books of a chef
        """
        book1 = Book.objects.create(chef=self.user)
        book2 = Book.objects.create(chef=self.user, book_type=Book.TO_SELL)

        url = '/0/chefs/%i/books' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('books', resp.data)
        self.assertEqual(1, len(resp.data['books']))
        keys = ('added', 'name', 'edit_date', 'chef', 'creation_date', 'id', 'nb_likes',
                'nb_recipes', 'book_type', 'status', 'price', 'product_id')
        self.assertEqual(set(keys), set(resp.data['books'][0].keys()))

    def test_get_photos(self):
        """
        Test get photos of a chef
        """
        recipe = Recipes.objects.create(chef=self.user, draft=False, private=False)
        photo = Photos.objects.create(recipe=recipe, photo_order=1)

        url = '/0/chefs/%i/photos' % self.user.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photos', resp.data)
        self.assertEqual(1, len(resp.data['photos']))
        keys = ('edit_date', 'creation_date', 'id', u'temperature', 'url', 'recipe', 'cover',
                'time', 'instructions', 'order', 'quantity')
        self.assertEqual(set(keys), set(resp.data['photos'][0].keys()))

    def test_search_suggested(self):
        """
        Test search "suggested" chefs
        """
        user2 = self.create_user('2')
        user3 = self.create_user('3')

        self.user.follow(user2)

        url = '/0/suggested/chefs'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('chefs', resp.data)
        self.assertEqual(4, len(resp.data['chefs']))
        self.assertEqual(self.CHEF_VIEW_KEYS - set(['followed']), set(resp.data['chefs'][0].keys()))
        self.assertEqual(user3.pk, resp.data['chefs'][3]['id'])


class ChefTransactionTest(ApiTestCase):
    @patch(SENDY_PATH)
    @patch(FACEBOOK_PATH)
    def test_signup_facebook(self, mocked_facebook, mocked_sendy):
        """
        Test registration with facebook
        """
        url = '/0/chefs'
        data = {
            'email': 'johndoe@example.com',
            'fb_access_token': 'TOKEN',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
        }
        mocked_facebook.return_value = {
            'id': '1401481816739108',
            'email': 'johndoe@example.com'
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

        # Test that we can log in
        url = '/0/chefs/login'
        data = {
            'email': 'johndoe@example.com',
            'fb_access_token': 'TOKEN',
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

        # Test that we cannot log in without password
        data_set = [
            {'email': 'johndoe@example.com'},
            {'email': 'johndoe@example.com', 'password': ''}]
        for data in data_set:
            resp = self.client.post(url, data=data)
            self.assertEqual(resp.status_code, 400)

    @patch(SENDY_PATH)
    @patch(FACEBOOK_PATH)
    def test_signup_login_facebook(self, mocked_facebook, mocked_sendy):
        """
        If a user tries to signup with a facebook token that is already present in the db
        login him instead of signing him up
        """
        url = '/0/chefs'
        data = {
            'email': 'johndoe@example.com',
            'fb_access_token': 'TOKEN',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
        }
        mocked_facebook.return_value = {
            'id': '1401481816739108',
            'email': 'johndoe@example.com'
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])

        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])

    @patch(SENDY_PATH)
    def test_signup_photo(self, mocked_sendy):
        """
        Test registration with a photo
        """
        url = '/0/chefs'
        data = {
            'email': 'johndoe@example.com',
            'password': 'secret',
            'name': 'John',
            'surname': 'Doe',
            'language': 'es',
            'photo': IMAGES['png'],
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])
        # Check that the photo exists
        self.assertTrue(Chefs.objects.last().avatar_photos.all())

    def test_get_chef_facebook_id(self):
        """
        Test get chef's facebook id
        """
        url = '/0/facebook'

        self.user.fb_user_id = 'FB_ID'
        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'fb_user_id': 'FB_ID'}})

    def test_set_chef_facebook_id(self):
        """
        Test set chef's facebook id
        """
        url = '/0/facebook'

        data = {'fb_user_id': 'FB_ID', 'fb_access_token': 'TOKEN'}

        resp = self.client.post(url, data)
        self.assertPermissionDenied(resp)

        headers = self.login()

        # Without data
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post(url, data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertEqual(Chefs.objects.get(pk=self.user.pk).fb_user_id, 'FB_ID')
        self.assertEqual(Chefs.objects.get(pk=self.user.pk).fb_access_token, 'TOKEN')

        # Cannot reset while set
        resp = self.client.post(url, data, **headers)
        self.assertEqual(resp.status_code, 400)

    def test_delete_chef_facebook_id(self):
        """
        Test delete chef's facebook id
        """
        url = '/0/facebook'

        self.user.fb_user_id = 'FB_ID'
        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertIsNone(Chefs.objects.get(pk=self.user.pk).fb_user_id)
        self.assertIsNone(Chefs.objects.get(pk=self.user.pk).fb_access_token)

    @patch(FACEBOOK_CONNECTIONS_PATH)
    def test_get_chef_facebook_friends_to_follow(self, mocked_facebook):
        """
        Test get chef's facebook friends to follow
        """
        url = '/0/facebook/friends'

        mocked_facebook.return_value = {
            'data': [
                {
                    'name': 'Friend1',
                    'id': 'FB_ID1'
                },
                {
                    'name': 'Friend2',
                    'id': 'FB_ID2'
                },
                {
                    'name': 'Friend3',
                    'id': 'FB_ID3'
                }
            ]
        }

        self.user.fb_user_id = 'FB_ID'
        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        chef1 = self.create_user('1')
        chef1.fb_user_id = 'FB_ID1'
        chef1.save()

        self.user.follow(chef1)

        chef2 = self.create_user('2')
        chef2.fb_user_id = 'FB_ID2'
        chef2.save()

        chef3 = self.create_user('3')
        chef3.fb_user_id = 'FB_NON_FRIEND'
        chef3.save()

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('friends', resp.data)
        self.assertEqual(1, len(resp.data['friends']))
        self.assertEqual(chef2.email, resp.data['friends'][0]['email'])
