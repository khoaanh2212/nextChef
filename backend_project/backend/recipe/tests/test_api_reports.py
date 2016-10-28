
from integration_tests.api_test_case import ApiTestCase

class ReportsTest(ApiTestCase):
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

    def test_report_recipe(self):
        """
        Test report recipe
        """
        recipe = self.create_recipe()
        url = '/0/recipes'
        url += '/%i/report' % recipe['id']

        resp = self.client.post(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('report', resp.data)
        keys = set(('id', 'chef', 'recipe', 'creation_date'))
        self.assertEqual(set(resp.data['report'].keys()), keys)

        data = {'subject': 'Subject'}
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('report', resp.data)
        keys = set(('id', 'chef', 'recipe', 'creation_date', 'subject'))
        self.assertEqual(set(resp.data['report'].keys()), keys)
