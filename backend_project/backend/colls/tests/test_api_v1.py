from colls.models import Collection, CollectionRecipes
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes


class APIV1CollsTest(ApiTestCase):
    def test_get_colls_list(self):
        """
        Test get colls
        """
        c1 = Collection.objects.create(is_active=True, name="collection 1")
        c2 = Collection.objects.create(is_active=False, name="collection 2")
        r1 = Recipes.objects.create(chef=self.user)
        CollectionRecipes.objects.create(collection=c1, recipe=r1)

        url = '/1/colls/list'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 405)

        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(len(resp.data['results']), 1)

        keys_coll = ('id', 'name', 'title1', 'title2', 'recipes', 'thumb')
        self.assertEqual(set(keys_coll), set(resp.data['results'][0].keys()))

        keys_recipe = ('id', 'name', 'url', 'public_url', 'chef', 'image_url', 'nb_likes',
                       'nb_comments', 'nb_added', 'nb_shares', 'added', 'shared', 'commented')
        self.assertEqual(set(keys_recipe), set(resp.data['results'][0]['recipes'][0].keys()))

        keys_chef = ('id', 'full_name', 'avatar', 'type_class')
        self.assertEqual(set(keys_chef), set(resp.data['results'][0]['recipes'][0]['chef'].keys()))
