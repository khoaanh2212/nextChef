import unittest
from mock import Mock, MagicMock

from domain.chefs.subscription.SubscriptionService import SubscriptionService

class SubscriptionServiceTest(unittest.TestCase):
    '''
        Subscription Service Test
    '''

    def setUp(self):
        self.repositoryStub = Mock()
        self.modelStub = Mock()
        self.sut = SubscriptionService.new(
            repository=self.repositoryStub,
            model=self.modelStub
        )

    def test_create_should_return_repository_result(self):
        self.repositoryStub.save.return_value = 'object'
        actual = self.sut.create('', '')
        self.assertEqual(actual, 'object')

    def test_update_should_update_the_subscription(self):
        self.repositoryStub.save.return_value = 'object'
        self.modelStub.update.return_value = 'updated-object'
        actual = self.sut.update('id', 'details')

        self.repositoryStub.save.assert_called_with('updated-object')
        self.assertEqual(actual, 'object')
