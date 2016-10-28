from integration_tests.api_test_case import ApiTestCase

from recipe.models import Recipes, Likes


class LikesTest(ApiTestCase):
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

    def test_like_recipe(self):
        """
        Test like/unlike recipe
        """
        recipe = self.create_recipe()
        url = '/0/recipes/%i/likes' % recipe['id']

        resp = self.client.post(url)
        self.assertPermissionDenied(resp)

        headers = self.login()

        # Like
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        # Cannot like more than once
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 400)

        # Unlike
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        # Recipe is not liked anymore
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 404)

    def test_get_recipe_likes(self):
        """
        Test get likes of a recipe
        """
        recipe = self.create_recipe()
        url = '/0/recipes/%i/likes' % recipe['id']

        recipe = Recipes.objects.get(pk=recipe['id'])
        users = [self.create_user(str(i)) for i in range(2, 5)]
        _ = [Likes.objects.create(chef=user, recipe=recipe) for user in users]

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(3, len(resp.data['results']))
