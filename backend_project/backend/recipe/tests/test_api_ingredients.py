from integration_tests.api_test_case import ApiTestCase


class IngredientsTest(ApiTestCase):
    def create_recipe(self):
        url = '/0/recipes'
        data = {
            'commensals': 1,
            'private': 1,
            'draft': 1,
            'name': 'Recipe',
            'ingredients': 'ingredient1\ningredient2',
            'tags': 'tag1 tag2',
        }
        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        return resp.data['recipe']

    def test_get_ingredients(self):
        """
        Test get ingredients
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/ingredients' % recipe['id']

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('ingredients', resp.data)
        ingredients = resp.data['ingredients']
        self.assertEqual(len(ingredients), 2)
        self.assertIn('id', ingredients[0])
        self.assertIn('name', ingredients[0])

    def test_add_ingredient(self):
        """
        Test add ingredient
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/ingredients' % recipe['id']

        data = {'name': 'ingredient3'}
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('ingredient', resp.data)
        ingredient = resp.data['ingredient']
        self.assertIn('id', ingredient)
        self.assertIn('name', ingredient)

    def test_delete_ingredient(self):
        """
        Test delete ingredient
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/ingredients/%i' % (recipe['id'], recipe['ingredients'][0]['id'])

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('response', resp.data)
        self.assertTrue(resp.data['response']['return'])
