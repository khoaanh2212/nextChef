import unittest

from books.models import Book
from chefs.models import Chefs, ChefFollows
from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes, Photos, Comments


class RecipesTest(ApiTestCase):
    def list_recipes(self, dynamic_url):
        url = dynamic_url
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

        resp_not_logged = self.client.get(url)
        self.assertEqual(resp_not_logged.status_code, 200)

        headers = self.login()
        resp_logged = self.client.get(url, **headers)
        self.assertEqual(resp_logged.status_code, 200)

        self.assertNotEqual(resp_not_logged.data['count'], resp_logged.data['count'])
        self.assertNotEqual(resp_not_logged.data['results'], resp_logged.data['results'])

        keys_recipe = (
            'id', 'name', 'url', 'public_url', 'serves', 'prep_time', 'creation_date', 'edit_date',
            'chef', 'image_url', 'comments', 'tags', 'products', 'ingredients', 'photos',
            'nb_likes', 'nb_added', 'nb_shares', 'nb_comments', 'added', 'shared', 'commented',
            'last_comments', 'description', 'to_sell')
        self.assertEqual(set(keys_recipe), set(resp_logged.data['results'][0].keys()))
        self.assertEqual(set(keys_recipe), set(resp_not_logged.data['results'][0].keys()))

        keys_chef = ('id', 'url', 'full_name', 'type_class', 'role', 'nb_followers', 'nb_loves',
                     'avatar', 'cover', 'location')
        self.assertEqual(set(keys_chef), set(resp_logged.data['results'][0]['chef'].keys()))
        self.assertEqual(set(keys_chef), set(resp_not_logged.data['results'][0]['chef'].keys()))

        keys_comments = ('id', 'chef', 'comment')
        self.assertEqual(set(keys_comments), set(resp_logged.data['results'][0]['comments'][0].keys()))
        self.assertEqual(set(keys_comments), set(resp_not_logged.data['results'][0]['comments'][0].keys()))

        keys_photos = ('id', 'instructions', 'image_url', 'photo_order')
        self.assertEqual(set(keys_photos), set(resp_logged.data['results'][0]['photos'][0].keys()))
        self.assertEqual(set(keys_photos), set(resp_not_logged.data['results'][0]['photos'][0].keys()))

    def list_recipes_following(self, dynamic_url):
        url = dynamic_url

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 403)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        keys_recipe = ('id', 'name', 'url', 'public_url', 'serves', 'prep_time', 'creation_date',
                       'edit_date', 'chef', 'image_url', 'comments', 'tags', 'products',
                       'ingredients', 'photos', 'nb_likes', 'nb_added', 'nb_shares', 'nb_comments',
                       'added', 'shared', 'commented', 'last_comments', 'description')
        self.assertEqual(set(keys_recipe), set(resp.data['results'][0].keys()))

        keys_chef = ('id', 'url', 'full_name', 'type_class', 'role', 'nb_followers', 'nb_loves',
                     'avatar', 'cover', 'location')
        self.assertEqual(set(keys_chef), set(resp.data['results'][0]['chef'].keys()))

        keys_comments = ('id', 'chef', 'comment')
        self.assertEqual(set(keys_comments), set(resp.data['results'][0]['comments'][0].keys()))

        keys_photos = ('id', 'instructions', 'image_url', 'photo_order')
        self.assertEqual(set(keys_photos), set(resp.data['results'][0]['photos'][0].keys()))

    def test_list_recipes(self):
        chefs = []
        chefs.append(Chefs.objects.create(email="foodie1@example.com", type=Chefs.TYPE_FOODIE))
        chefs.append(Chefs.objects.create(email="foodie2@example.com", type=Chefs.TYPE_FOODIE))
        chefs.append(Chefs.objects.create(email="pro1@example.com", type=Chefs.TYPE_PRO))
        chefs.append(Chefs.objects.create(email="pro2@example.com", type=Chefs.TYPE_PRO))
        chefs.append(Chefs.objects.create(email="comment@example.com"))

        ChefFollows.objects.create(follower=self.user, following=chefs[0])
        ChefFollows.objects.create(follower=self.user, following=chefs[2])

        for chef in chefs:
            r = Recipes.objects.create(chef=chef, private=False, draft=False)
            Comments.objects.create(recipe=r, chef=chefs[-1])
            for i in range(0, 4):
                Photos.objects.create(recipe=r)
            r.cache_photos = 4
            r.save()

        #Recipes all
        dynamic_url = '/1/recipes/list/recipes'
        self.list_recipes(dynamic_url)

        #Recipes pro
        dynamic_url = '/1/recipes/list/recipes/pro'
        self.list_recipes(dynamic_url)

        #Recipes foodie
        dynamic_url = '/1/recipes/list/recipes/foodie'
        self.list_recipes(dynamic_url)

        #Recipes following
        dynamic_url = '/1/recipes/list/followings'
        #self.list_recipes_following(dynamic_url)

    @unittest.skip('Broken. Fix it (Redis patching required)')
    def test_search(self):
        """
        Test search recipes
        """
        user2 = self.create_user('2')
        user3 = self.create_user('3')
        self.user.follow(user2)

        for user in user2, user3:
            for i in range(0, 10):
                recipe = Recipes.objects.create(chef=user, private=False, draft=False)
                for i in range(0, 5):
                    Photos.objects.create(recipe=recipe)
                recipe.cache_photos = 5
                recipe.save()
            for i in range(0, 5):
                book = Book.objects.create(chef=user, book_type=Book.TO_SELL)

        url = '/1/explore'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('recipes', resp.data)
        self.assertEqual(6, len(resp.data['recipes']))
        self.assertEqual(user2.pk, resp.data['recipes'][0]['chef']['id'])

        url = '/1/recommended'
        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('recipes', resp.data)
        self.assertIn('books', resp.data)
        self.assertEqual(6, len(resp.data['recipes']))
        self.assertEqual(3, len(resp.data['books']))
        self.assertEqual(user3.pk, resp.data['recipes'][0]['chef']['id'])
