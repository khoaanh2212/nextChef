from integration_tests.api_test_case import ApiTestCase

from recipe.models import Recipes, Shares


class SharesTest(ApiTestCase):
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

    def test_share_recipe(self):
        """
        Test share recipe
        """
        recipe = self.create_recipe()
        url = '/0/recipes/%i/shares' % recipe['id']

        resp = self.client.post(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('share', resp.data)
        keys = set(('id', 'chef', 'recipe', 'creation_date'))
        self.assertEqual(set(resp.data['share'].keys()), keys)

        data = {'via': 'Via'}
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('share', resp.data)
        keys = set(('id', 'chef', 'recipe', 'creation_date', 'via'))
        self.assertEqual(set(resp.data['share'].keys()), keys)

    def test_get_recipe_shares(self):
        """
        Test get shares of a recipe
        """
        recipe = self.create_recipe()
        url = '/0/recipes/%i/shares' % recipe['id']

        recipe = Recipes.objects.get(pk=recipe['id'])
        users = [self.create_user(str(i)) for i in range(2, 5)]
        _ = [Shares.objects.create(chef=user, recipe=recipe) for user in users]

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(3, len(resp.data['results']))
