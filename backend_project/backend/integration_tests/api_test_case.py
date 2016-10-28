import hashlib
import logging
from urllib import urlencode

import cssutils
from django.test import Client
from mock import patch

from chefs.models import Chefs
from integration_tests.integration_test_case import IntegrationTestCase

SENDY_PATH = 'pysendy.Sendy.subscribe'


class ApiTestClient(Client):
    def put(self, *args, **kwargs):
        data = kwargs.get('data')
        if isinstance(data, dict):
            data = urlencode(data)
            kwargs['data'] = data
            kwargs['content_type'] = 'application/x-www-form-urlencoded'
        return super(ApiTestClient, self).put(*args, **kwargs)


class ApiTestCase(IntegrationTestCase):
    client_class = ApiTestClient

    def __init__(self, methodName='runTest'):
        super(IntegrationTestCase, self).__init__(methodName)
        self.user = None
        self.cssutils_loglevel = None

    @patch(SENDY_PATH)
    def setUp(self, mocked_sendy):
        super(ApiTestCase, self).setUp()
        self.user = Chefs.objects.create_user('Test', 'Tests', 'test@example.com', 'secret')
        self.cssutils_loglevel = cssutils.log.getEffectiveLevel()
        cssutils.log.setLevel(logging.CRITICAL)

    def tearDown(self):
        cssutils.log.setLevel(self.cssutils_loglevel)
        super(ApiTestCase, self).tearDown()

    def login(self):
        url = '/0/chefs/login'
        data = {'email': 'test@example.com', 'password': hashlib.md5('secret').hexdigest()}
        resp = self.client.post(url, data=data)
        token = resp.data['auth']['token']
        return {'HTTP_CB_AUTH': token}

    def assertPermissionDenied(self, resp):
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, "No user credentials\n")

    def assertInvalidCredentials(self, resp):
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, "Invalid user credentials\n")

    def create_user(self, append):
        s = append
        return Chefs.objects.create_user('Test' + s, 'Tests', 'test' + s + '@example.com', 'secret')
