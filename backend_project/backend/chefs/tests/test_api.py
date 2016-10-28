import hashlib

import facebook
from mock import patch

from integration_tests.api_test_case import ApiTestCase

FACEBOOK_PATH = 'facebook.GraphAPI.get_object'
FACEBOOK_CONNECTIONS_PATH = 'facebook.GraphAPI.get_connections'

# 1px base64 encoded images
IMAGES = {
    'gif': 'R0lGODdhAQABAIABADPxL////ywAAAAAAQABAAACAkQBADs=',

    'jpg': '/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/2wBDAAMCAg'
           'MCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUV'
           'DA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFB'
           'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wgARCAABAAEDAREAAhEBAxEB'
           '/8QAFAABAAAAAAAAAAAAAAAAAAAABv/EABQBAQAAAAAAAAAAAAAAAAAAAAf/2gAMAw'
           'EAAhADEAAAAVpQK//EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAQUCf//EABQR'
           'AQAAAAAAAAAAAAAAAAAAAAD/2gAIAQMBAT8Bf//EABQRAQAAAAAAAAAAAAAAAAAAAA'
           'D/2gAIAQIBAT8Bf//EABQQAQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEABj8Cf//EABQQ'
           'AQAAAAAAAAAAAAAAAAAAAAD/2gAIAQEAAT8hf//aAAwDAQACAAMAAAAQ/wD/xAAUEQ'
           'EAAAAAAAAAAAAAAAAAAAAA/9oACAEDAQE/EH//xAAUEQEAAAAAAAAAAAAAAAAAAAAA'
           '/9oACAECAQE/EH//xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAE/EH//2Q==',
    'png': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAACXBIWXMAAAsTAAALEw'
           'EAmpwYAAAAB3RJTUUH3ggPDBkdfe+wzQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRl'
           'ZCB3aXRoIEdJTVBkLmUHAAAADElEQVQI12Mw/qgPAAKuAVQdNCeBAAAAAElFTkSuQm'
           'CC',
}


class AuthTest(ApiTestCase):
    def test_login(self):
        """
        Test login
        """
        url = '/0/chefs/login'

        data = {'email': self.user.email, 'password': 'secret'}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'message': 'Bad credentials', 'code': 401})

        data = {'email': self.user.email, 'password': hashlib.md5('secret').hexdigest()}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])

    def test_login_fail(self):
        """
        Test login for nonexistent user
        """
        url = '/0/chefs/login'
        data = {'email': 'test2@example.com', 'password': 'secret'}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'message': 'chef do not exists', 'code': 404})

    def test_logout(self):
        """
        Test logout
        """
        url = '/0/chefs/login'
        resp = self.client.delete(url)
        self.assertPermissionDenied(resp)

        headers = self.login()
        resp = self.client.delete(url, **headers)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.delete(url, **headers)
        self.assertPermissionDenied(resp)

    def test_reset_password(self):
        """
        Test reset password
        """
        url = '/0/chefs/resetpassword'

        resp = self.client.put(url, data={'email': self.user.email})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, {'response': {'return': True}})

        # Test fail
        resp = self.client.put(url, data={'email': 'fake'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data, {'code': 400, 'message': 'No chef found'})


class AuthTransactionTest(ApiTestCase):
    @patch(FACEBOOK_PATH)
    def test_login_facebook(self, mocked_facebook):
        """
        Test login Facebook
        """
        url = '/0/chefs/login'

        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        mocked_facebook.return_value = {'id': '1401481816739108', 'email': 'test@example.com'}

        data = {'email': 'test@example.com', 'fb_access_token': 'TOKEN'}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('auth', resp.data)
        self.assertIn('token', resp.data['auth'])

    @patch(FACEBOOK_PATH)
    def test_login_facebook_fail(self, mocked_facebook):
        """
        Test login Facebook call fails
        """
        url = '/0/chefs/login'

        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        mocked_facebook.side_effect = facebook.GraphAPIError(None)

        data = {'email': 'test@example.com', 'fb_access_token': 'TOKEN'}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 403)

    @patch(FACEBOOK_PATH)
    def test_login_facebook_fail_email(self, mocked_facebook):
        """
        Test login Facebook fail because emails don't match
        """
        url = '/0/chefs/login'

        self.user.fb_access_token = 'TOKEN'
        self.user.save()

        mocked_facebook.return_value = {'id': '1401481816739108', 'email': 'bad@notexample.com'}

        data = {'email': 'test@example.com', 'fb_access_token': 'TOKEN'}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 403)
