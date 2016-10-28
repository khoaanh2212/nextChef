from integration_tests.api_test_case import ApiTestCase


class TagsTest(ApiTestCase):
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

    def test_get_tags(self):
        """
        Test get tags
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/tags' % recipe['id']

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('tags', resp.data)
        tags = resp.data['tags']
        self.assertEqual(len(tags), 2)
        self.assertIn('id', tags[0])
        self.assertIn('name', tags[0])

    def test_add_tag(self):
        """
        Test add tag
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/tags' % recipe['id']

        data = {'name': 'tag3'}
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('tag', resp.data)
        tag = resp.data['tag']
        self.assertIn('id', tag)
        self.assertIn('name', tag)

    def test_delete_tag(self):
        """
        Test delete tag
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/tags/%i' % (recipe['id'], recipe['tags'][0]['id'])

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('response', resp.data)
        self.assertTrue(resp.data['response']['return'])
