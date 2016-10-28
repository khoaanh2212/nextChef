from base64 import b64decode

from django.core.files.base import ContentFile

from chefs.tests.test_api import IMAGES
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes, Photos, ChefsHasRecipes, PhotoFilters


class PhotosTest(ApiTestCase):
    def create_recipe(self):
        url = '/0/recipes'
        data = {
            'commensals': 1,
            'private': 1,
            'draft': 1,
            'name': 'Recipe',
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        return resp.data['recipe']

    def test_photo(self):
        """
        Test photo whole cycle
        """
        recipe = self.create_recipe()
        url = '/0/recipes'

        # Create
        url += '/%i/photos' % recipe['id']
        data = {
            'file': IMAGES['png'],
            'instructions': 'instructions',
            'time': 'time',
            'temperature': 'temperature',
            'quantity': 'quantity',
            'cover': 1,
            'order': 10,
        }
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photo', resp.data)
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['photo']))
        photo_id = resp.data['photo']['id']
        self.assertEqual(Photos.objects.last().temperature, data['temperature'])

        # Update
        url += '/%i' % photo_id
        data = {'temperature': 'new temperature'}
        resp = self.client.put(url, data=data)
        self.assertPermissionDenied(resp)
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Photos.objects.last().temperature, data['temperature'])

        # Read
        url = '/0/recipes'
        url += '/%i/photos' % recipe['id']
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photos', resp.data)
        self.assertEqual(1, len(resp.data['photos']))
        keys = set(('id', 'url', 'creation_date', 'edit_date', 'instructions', 'time',
                    'temperature', 'quantity', 'recipe', 'cover', 'order'))
        self.assertEqual(keys, set(resp.data['photos'][0]))

        # Delete
        url += '/%i' % photo_id
        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})
        self.assertEqual(Photos.objects.count(), 0)

    def test_updated_photos(self):
        """
        Test get latest update photos
        """
        url = '/0/updated/photos'

        moment = 1 # Epoch start
        user2 = self.create_user('2')

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

        ChefsHasRecipes.objects.create(chef=self.user, recipe=recipe2)
        ChefsHasRecipes.objects.create(chef=self.user, recipe=recipe3)
        ChefsHasRecipes.objects.create(chef=self.user, recipe=recipe4)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.get(url, data={'date': moment}, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('photos', resp.data)
        self.assertEqual(2, len(resp.data['photos']))
        keys = set(('id', 'url', 'creation_date', 'edit_date', 'instructions', 'time',
                    'temperature', 'quantity', 'recipe', 'cover', 'order'))
        self.assertEqual(keys, set(resp.data['photos'][0]))


class PhotosStylesTest(ApiTestCase):
    def test_styles(self):
        self.skipTest('skipped PhotosStylesTest.test_styles')
        """
        Test get style
        """
        image = ContentFile(b64decode(IMAGES['gif']), name='temp.gif')

        filter_ = PhotoFilters.objects.create(name="filter1", type="Type")
        photo = Photos.objects.create(s3_url=image)
        url = '/0/styles/photos_url/%i/%s' % (photo.pk, filter_.name)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('style', resp.data)
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['style']))

    def test_styles_old_url(self):
        self.skipTest('skipped PhotosStylesTest.test_styles_old_url')
        """
        Test get style from the legacy url
        """
        image = ContentFile(b64decode(IMAGES['gif']), name='temp.gif')

        filter_ = PhotoFilters.objects.create(name="filter1", type="Type")
        photo = Photos.objects.create(s3_url=image)
        url = '/0/styles/photos/%i/%s' % (photo.pk, filter_.name)

        resp = self.client.get(url, allow_redirects=False)
        self.assertEqual(resp.status_code, 302)
