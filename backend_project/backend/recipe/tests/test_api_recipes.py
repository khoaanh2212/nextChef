from chefs.tests.test_api import IMAGES
from integration_tests.api_test_case import ApiTestCase

from recipe.models import Recipes, ChefsHasRecipes, Photos


class RecipesTest(ApiTestCase):
    KEYS = set((
        'id', 'creation_date', 'edit_date', 'ingredients', 'chef', 'tags', 'public_url',
        'commensals', 'private', 'added', 'draft', 'liked', 'shared', 'reported', 'commented',
        'products', 'prep_time', 'serves', 'nb_shares', 'nb_likes', 'name', 'nb_comments',
        'nb_added', 'bought', 'book_for_sale', 'description',
    ))

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

    def test_add_recipe(self):
        """
        Test add recipe
        """
        url = '/0/recipes'

        # Minimum required fields
        data = {
            'commensals': 0,
            'private': 0,
            'draft': 0,
        }
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        keys = self.KEYS - set(('name', 'nb_shares', 'nb_likes', 'nb_comments', 'nb_added'))
        self.assertEqual(keys, set(resp.data['recipe'].keys()))

        keys = 'id', 'type', 'email', 'name', 'surname'
        self.assertEqual(set(keys), set(resp.data['recipe']['chef'].keys()))

        recipe = resp.data['recipe']
        self.assertNotIn('name', recipe)
        self.assertEqual(recipe['commensals'], 0)
        self.assertEqual(recipe['private'], 0)
        self.assertEqual(recipe['draft'], 0)
        self.assertEqual(len(recipe['ingredients']), 0)
        self.assertEqual(len(recipe['tags']), 0)

        # Will all possible params
        data = {
            'commensals': 1,
            'private': 1,
            'draft': 1,
            'name': 'Recipe',
            'ingredients': 'ingredient1\ningredient2',
            'tags': 'tag1 tag2',
        }

        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        recipe = resp.data['recipe']
        self.assertEqual(recipe['name'], 'Recipe')
        self.assertEqual(recipe['commensals'], 1)
        self.assertEqual(recipe['private'], 1)
        self.assertEqual(recipe['draft'], 1)
        self.assertEqual(len(recipe['ingredients']), 2)
        self.assertEqual(len(recipe['tags']), 2)

    def test_update_recipe(self):
        """
        Test update recipe
        """
        url = '/0/recipes'

        data = {
            'commensals': 0,
            'private': 0,
            'draft': 0,
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)

        url += '/%i' % resp.data['recipe']['id']
        data = {}
        resp = self.client.put(url, data=data)
        self.assertPermissionDenied(resp)

        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        recipe = resp.data['recipe']
        self.assertNotIn('name', recipe)
        self.assertEqual(recipe['commensals'], 0)
        self.assertEqual(recipe['private'], 0)
        self.assertEqual(recipe['draft'], 0)
        self.assertEqual(len(recipe['ingredients']), 0)
        self.assertEqual(len(recipe['tags']), 0)

        data = {
            'commensals': 1,
            'private': 1,
            'draft': 1,
            'name': 'Recipe',
            'ingredients': 'ingredient1\ningredient2',
            'tags': 'tag1 tag2',
        }
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        recipe = resp.data['recipe']
        self.assertEqual(recipe['name'], 'Recipe')
        self.assertEqual(recipe['commensals'], 1)
        self.assertEqual(recipe['private'], 1)
        self.assertEqual(recipe['draft'], 1)
        self.assertEqual(len(recipe['ingredients']), 2)
        self.assertEqual(len(recipe['tags']), 2)

    def test_delete_recipe(self):
        """
        Test delete recipe
        """
        url = '/0/recipes'

        data = {
            'commensals': 0,
            'private': 0,
            'draft': 0,
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        self.assertTrue(Recipes.objects.exists())

        url += '/%i' % resp.data['recipe']['id']
        resp = self.client.delete(url, data={}, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertFalse(Recipes.objects.exists())

    def test_view_recipe(self):
        """
        Test view recipe
        """
        url = '/0/recipes'

        data = {
            'commensals': 0,
            'private': 0,
            'draft': 0,
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)

        url += '/%i' % resp.data['recipe']['id']
        resp = self.client.get(url, data={}, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        keys = self.KEYS - set(('name', ))
        self.assertEqual(keys, set(resp.data['recipe'].keys()))

        # If the chef has a photo make sure it is included
        self.assertNotIn('photo', resp.data['recipe']['chef'])
        self.user.avatar_photos.create(s3_url='image')  # Create photo
        resp = self.client.get(url, data={}, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photo', resp.data['recipe']['chef'])
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['recipe']['chef']['photo']))

    def test_view_recipe_with_photo(self):
        """
        Test view recipe with photo
        """
        url = '/0/recipes'

        data = {
            'commensals': 0,
            'private': 0,
            'draft': 0,
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        recipe_id = resp.data['recipe']['id']

        photo_url = url + '/%i/photos' % recipe_id
        data = {
            'file': IMAGES['png'],
            'instructions': 'instructions',
            'time': 'time',
            'temperature': 'temperature',
            'quantity': 'quantity',
            'cover': 1,
            'order': 10,
        }
        resp = self.client.post(photo_url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photo', resp.data)

        url += '/%i' % recipe_id
        resp = self.client.get(url, data={}, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        self.assertIn('cover_photo', resp.data['recipe'])
        keys = set(('url', 'id', 'edit_date', 'creation_date'))
        self.assertEqual(keys, set(resp.data['recipe']['cover_photo']))

    def test_view_recipe_draft(self):
        """
        Test view recipe draft
        """
        url = '/0/recipes'
        data = {
            'commensals': 0,
            'private': 0,
            'draft': 1,
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)

        url += '/%i' % resp.data['recipe']['id']
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get(url, data={'draft': 1}, **headers)
        self.assertEqual(resp.status_code, 200)

    def test_copy_recipe(self):
        """
        Test copy recipe
        """
        user2 = self.create_user('2')
        recipe = self.create_recipe()
        recipe = Recipes.objects.get(pk=recipe['id'])
        recipe.chef = user2
        recipe.save()

        url = '/0/recipes/%i' % recipe.pk
        resp = self.client.generic('copy', url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.generic('copy', url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipe', resp.data)
        keys = self.KEYS - set(('nb_shares', 'nb_likes', 'nb_comments', 'nb_added'))
        self.assertEqual(keys, set(resp.data['recipe'].keys()))

        keys = 'id', 'type', 'email', 'name', 'surname'
        self.assertEqual(set(keys), set(resp.data['recipe']['chef'].keys()))

        # Do not fail if trying to copy it again
        resp = self.client.generic('copy', url, **headers)
        self.assertEqual(resp.status_code, 200)

    def test_search_explore(self):
        """
        Test search "explore" recipes
        """
        user2 = self.create_user('2')
        user3 = self.create_user('3')

        recipe1 = self.create_recipe()
        recipe1 = Recipes.objects.last()
        recipe1.chef = user2
        recipe1.save()

        recipe2 = self.create_recipe()
        recipe2 = Recipes.objects.last()
        recipe2.chef = user2
        recipe2.save()

        recipe3 = self.create_recipe()
        recipe3 = Recipes.objects.last()
        recipe3.chef = user3
        recipe3.save()

        self.user.follow(user2)
        ChefsHasRecipes.objects.create(chef=self.user, recipe=recipe2)

        url = '/0/explore/new'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipes', resp.data)
        self.assertEqual(1, len(resp.data['recipes']))
        self.assertEqual(self.KEYS, set(resp.data['recipes'][0].keys()))
        self.assertEqual(recipe1.pk, resp.data['recipes'][0]['id'])

    def test_search_new(self):
        """
        Test search "new" recipes
        """
        user2 = self.create_user('2')

        recipe1 = self.create_recipe()
        recipe1 = Recipes.objects.last()
        recipe1.chef = user2
        recipe1.save()

        for i in range(4):
            Photos.objects.create(recipe=recipe1)
        recipe1.cache_photos = 4
        recipe1.save()

        url = '/0/new/recipes'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipes', resp.data)
        self.assertEqual(1, len(resp.data['recipes']))
        self.assertEqual(self.KEYS, set(resp.data['recipes'][0].keys()))

    def test_search_updated(self):
        """
        Test search "updated" recipes
        """
        self.create_recipe()

        url = '/0/updated/recipes'
        params = {'date': 1}
        resp = self.client.get(url, data=params)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, data=params, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('recipes', resp.data)
        self.assertEqual(1, len(resp.data['recipes']))
        self.assertEqual(self.KEYS, set(resp.data['recipes'][0].keys()))
