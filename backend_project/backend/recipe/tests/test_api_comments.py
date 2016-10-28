from integration_tests.api_test_case import ApiTestCase

from recipe.models import Recipes, Comments


class TagsTest(ApiTestCase):
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
        ret = resp.data['recipe']
        recipe = Recipes.objects.get(pk=ret['id'])
        comment = Comments.objects.create(recipe=recipe, chef=self.user, comment='The Comment')
        return ret

    def test_get_comments(self):
        """
        Test get comments
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/comments' % recipe['id']

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('comments', resp.data)
        comments = resp.data['comments']
        self.assertEqual(len(comments), 1)
        self.assertIn('id', comments[0])
        self.assertIn('comment', comments[0])
        self.assertIn('chef', comments[0])
        self.assertIn('id', comments[0]['chef'])
        self.assertIn('name', comments[0]['chef'])

    def test_add_comment(self):
        """
        Test add comment
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/comments' % recipe['id']

        data = {'comment': 'the comment'}
        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('comment', resp.data)
        comment = resp.data['comment']
        self.assertIn('id', comment)
        self.assertIn('comment', comment)
