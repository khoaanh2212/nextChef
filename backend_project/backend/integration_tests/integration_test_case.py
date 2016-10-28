from django.test import TestCase

from django.core.management import call_command


class IntegrationTestCase(TestCase):
    has_been_created = False

    def __init__(self, methodName='runTest'):
        super(IntegrationTestCase, self).__init__(methodName)

    @classmethod
    def setUpClass(cls):
        if not IntegrationTestCase.has_been_created:
            IntegrationTestCase.has_been_created = True
            call_command('syncdb')
            call_command('migrate')

    def setUp(self):
        super(IntegrationTestCase, self).setUp()

    def tearDown(self):
        super(IntegrationTestCase, self).tearDown()
