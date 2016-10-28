from integration_tests.api_test_case import ApiTestCase


class FollowTest(ApiTestCase):
    CHEF_KEYS = set((
        'country', 'creation_date', 'edit_date', 'email', 'id', 'interests', 'language',
        'languages', 'location', 'name', 'nb_books', 'nb_followers', 'nb_followings', 'nb_likes',
        'nb_recipes', 'offline', 'private_recipes', 'referents', 'short_bio', 'surname', 'type',
        'username', 'cover',
    ))

    def test_follow(self):
        """
        Test follow a chef
        """
        chef2 = self.create_user('2')
        url = '/0/chefs/%i/follows' % chef2.pk

        resp = self.client.post(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_follow_self(self):
        """
        Test follow self
        """
        url = '/0/chefs/%i/follows' % self.user.pk

        headers = self.login()
        resp = self.client.post(url, **headers)
        self.assertEqual(resp.status_code, 400)

    def test_follow_show(self):
        """
        Test show chef follow relation
        """
        chef2 = self.create_user('2')
        url = '/0/chefs/%i/follows' % chef2.pk

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 404)

        self.user.follow(chef2)
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_unfollow(self):
        """
        Test unfollow chef
        """
        chef2 = self.create_user('2')
        url = '/0/chefs/%i/follows' % chef2.pk

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 404)

        self.user.follow(chef2)
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

    def test_following(self):
        """
        Test following
        """
        url = '/0/chefs/%i/following' % self.user.pk

        chef2 = self.create_user('2')
        self.user.follow(chef2)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('following', resp.data)
        self.assertEqual(1, len(resp.data['following']))
        self.assertEqual(self.CHEF_KEYS, set(resp.data['following'][0].keys()))

        # Check 'most_popular_recipe_cover_image' is present if it has to
        self.assertNotIn('most_popular_recipe_cover_image', resp.data['following'][0])
        r = chef2.recipes.create(private=False, draft=False)
        p = r.photos.create(is_cover=True, s3_url='image')
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('most_popular_recipe_cover_image', resp.data['following'][0])
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['following'][0]['most_popular_recipe_cover_image']))

    def test_followers(self):
        """
        Test followers
        """
        url = '/0/chefs/%i/followers' % self.user.pk

        chef2 = self.create_user('2')
        chef2.follow(self.user)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('followers', resp.data)
        self.assertEqual(1, len(resp.data['followers']))
        self.assertEqual(self.CHEF_KEYS, set(resp.data['followers'][0].keys()))

        # Check 'most_popular_recipe_cover_image' is present if it has to
        self.assertNotIn('most_popular_recipe_cover_image', resp.data['followers'][0])
        r = chef2.recipes.create(private=False, draft=False)
        p = r.photos.create(is_cover=True, s3_url='image')
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('most_popular_recipe_cover_image', resp.data['followers'][0])
        keys = set(('id', 'url', 'creation_date', 'edit_date'))
        self.assertEqual(keys, set(resp.data['followers'][0]['most_popular_recipe_cover_image']))
