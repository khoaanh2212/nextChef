from chefs.models import Chefs
from integration_tests.api_test_case import ApiTestCase
from notifications.models import Notification, NotificationType, Device
from recipe.models import Recipes, Comments


def creation_notification_types():
    ret = {}
    for name in 'LIKE', 'COMMENT', 'COPY_RECIPE', 'FOLLOW', 'NORMAL':
        n, _ = NotificationType.objects.get_or_create(name=name.lower())
        ret[name] = n
    return ret


class NotificationsTest(ApiTestCase):
    def setUp(self):
        super(NotificationsTest, self).setUp()
        self.types = creation_notification_types()

    def test_get_notifications(self):
        """
        Test get notifications
        """
        url = '/0/notifications'

        user2 = Chefs.objects.create()
        recipe = Recipes.objects.create()
        comment = Comments.objects.create()

        Notification.objects.create(chef=self.user, creator=user2, recipe=recipe, comment=comment,
                                    type=self.types['LIKE'])

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('notifications', resp.data)
        keys = ('id', 'chef', 'comment', 'creation_date', 'creator', 'edit_date', 'message',
                'recipe', 'type', 'unread', 'deeplink', 'followed')
        self.assertEqual(1, len(resp.data['notifications']))
        self.assertEqual(set(keys), set(resp.data['notifications'][0].keys()))

        # Recipe
        keys = ('added', 'commensals', 'commented', 'creation_date', 'draft', 'edit_date', 'id',
                'ingredients', 'liked', 'name', 'nb_added', 'nb_comments', 'nb_likes', 'nb_shares',
                'private', 'public_url', 'reported', 'shared', 'tags')
        self.assertEqual(set(keys), set(resp.data['notifications'][0]['recipe'].keys()))

        # Comment
        keys = ('id', )
        self.assertEqual(set(keys), set(resp.data['notifications'][0]['comment'].keys()))

        # Type
        keys = ('id', 'name', 'creation_date', 'edit_date')
        self.assertEqual(set(keys), set(resp.data['notifications'][0]['type'].keys()))

        # Chef and creator
        keys = ('id', 'email', 'name', 'surname', 'type')
        self.assertEqual(set(keys), set(resp.data['notifications'][0]['chef'].keys()))
        self.assertEqual(set(keys), set(resp.data['notifications'][0]['creator'].keys()))


    def test_get_notifications_unread(self):
        """
        Test get unread notifications
        """
        url = '/0/notifications/unread'

        Notification.objects.create(chef=self.user)
        Notification.objects.create(chef=self.user)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': 2}})

    def test_update_notification(self):
        """
        Test update notification
        """
        notification = Notification.objects.create(chef=self.user)

        url = '/0/notifications/%i' % notification.pk
        data = {'unread': 0}

        self.assertTrue(notification.unread)

        resp = self.client.put(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        notification = Notification.objects.last()
        self.assertFalse(notification.unread)

        # Reverse
        data = {'unread': 1}
        resp = self.client.put(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        notification = Notification.objects.last()
        self.assertTrue(notification.unread)

    def test_delete_notification(self):
        """
        Test delete notification
        """
        notification = Notification.objects.create(chef=self.user)

        url = '/0/notifications/%i' % notification.pk

        self.assertEqual(1, Notification.objects.count())

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        self.assertEqual(0, Notification.objects.count())


class DevicesTest(ApiTestCase):
    def test_create_device(self):
        """
        Test create device
        """
        url = '/0/notifications/devices'

        data = {
            'type': 'android',
            'identificator': 'identificator',
            'environment': 'environment',
            'language': 'es',
        }

        resp = self.client.post(url, data=data)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('device', resp.data)
        keys = ('id', 'chef', 'creation_date', 'edit_date', 'environment', 'identificator', 'type',
                'language')
        self.assertEqual(set(keys), set(resp.data['device'].keys()))

        # Test special behaviour
        self.assertEqual(1, Device.objects.count())
        device = Device.objects.last()
        self.assertEqual(device.type, 'android')

        data = {
            'type': 'ios',
            'identificator': 'identificator',
        }
        resp = self.client.post(url, data=data, **headers)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(1, Device.objects.count())
        device = Device.objects.get(pk=device.pk)
        self.assertEqual(device.type, 'android')

    def test_get_devices(self):
        """
        Test get devices
        """
        url = '/0/notifications/devices'

        device = Device.objects.create(chef=self.user)

        resp = self.client.get(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.get(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('devices', resp.data)
        keys = ('id', 'chef', 'creation_date', 'edit_date', 'environment', 'identificator', 'type',
                'language')
        self.assertEqual(1, len(resp.data['devices']))
        self.assertEqual(set(keys), set(resp.data['devices'][0].keys()))

    def test_delete_device(self):
        """
        Test delete devices
        """
        device = Device.objects.create(chef=self.user)
        url = '/0/notifications/devices/%i' % device.pk

        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        self.assertEqual(0, Device.objects.count())
