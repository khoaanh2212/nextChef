from banners.models import Banner
from integration_tests.api_test_case import ApiTestCase


class APIV1BannersTest(ApiTestCase):
    def test_get_banners_list(self):
        """
        Test get banners
        """
        b1 = Banner.objects.create(is_active=True)
        b2 = Banner.objects.create(is_active=False)

        url = '/1/banners/list'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data['results']), 1)
        keys = ('id', 'title', 'subtitle', 'text', 'url', 'type', 'thumb')
        self.assertEqual(set(keys), set(resp.data['results'][0].keys()))
