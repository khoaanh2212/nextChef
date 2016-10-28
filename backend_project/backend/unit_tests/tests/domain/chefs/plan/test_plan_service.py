import unittest
import mock

from domain.chefs.plan.PlanService import PlanService

class PlanServiceTest(unittest.TestCase):
    '''
        Plan Service Test
    '''

    def setUp(self):
        self.sut = PlanService()

    def test_create_should_call_to_repository_with_model_object(self):
        self.sut.repository.save = mock.MagicMock(name='insert')
        self.sut.model.create = mock.MagicMock(name='create')
        self.sut.repository.save.return_value = 'plan-object'
        self.sut.model.create.return_value = 'plan-object'

        actual = self.sut.create('type', 'interval', 5)

        self.sut.repository.save.assert_called_with('plan-object')
        self.assertEqual(actual, 'plan-object')

    def test_getPlanByTypeAndInterval_should_call_to_repository(self):
        self.sut.repository.findByTypeAndInterval = mock.MagicMock(name='insert')
        self.sut.repository.findByTypeAndInterval.return_value = 'plan-object'

        actual = self.sut.getPlanByTypeAndInterval('type', 'interval')

        self.sut.repository.findByTypeAndInterval.assert_called_with('type', 'interval')
        self.assertEqual(actual, 'plan-object')
