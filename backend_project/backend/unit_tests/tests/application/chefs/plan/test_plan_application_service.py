# -*- coding: utf-8 -*-
import unittest
import mock
import datetime

from application.chefs.plan.PlanApplicationService import PlanApplicationService
from domain.chefs.plan.Plan import Plan

class PlanApplicationServiceTest(unittest.TestCase):
    '''
        Plan Application Service Unit Tests
    '''

    def setUp(self):
        self.sut = PlanApplicationService()
        self.sut.service.getPlanByTypeAndInterval = mock.MagicMock(name='getPlanByTypeAndInterval')
        datetime_patcher = mock.patch.object(
            datetime, 'datetime',
            mock.Mock(wraps=datetime.datetime)
        )
        mocked_datetime = datetime_patcher.start()
        mocked_datetime.today.return_value = datetime.datetime(2015, 1, 1)
        self.addCleanup(datetime_patcher.stop)

    def test_getPlanByTypeAndInterval_should_call_plan_service_getPlanByTypeAndInterval(self):
        self.__set_up_plan()
        self.sut.service.getPlanByTypeAndInterval.assert_called_with('type', 'monthly')

    def test_getPlanByTypeAndInterval_should_return_and_object_with_1_month_due_date_if_interval_monthly(self):
        actual = self.__set_up_plan()
        self.assertEqual(actual['due_date'], datetime.datetime(2015, 1, 31))

    def test_getPlanByTypeAndInterval_should_return_and_object_with_1_year_due_date_if_interval_annually(self):
        actual = self.__set_up_plan('type', 'annually')
        self.assertEqual(actual['due_date'], datetime.datetime(2016, 1, 1))

    def test_getPlanByTypeAndInterval_should_return_expected_value(self):
        plan = self.__mkPlan('type', 'monthly', 5)
        self.sut.service.getPlanByTypeAndInterval.return_value = plan
        expected = dict( plan=plan, due_date=datetime.datetime(2015, 1, 31), amount=5 )
        actual = self.sut.getPlanByTypeAndInterval('type', 'monthly')
        self.assertEqual(actual, expected)

    def __mkPlan(self, type='type', interval='monthly', amount_per_month=5):
        return Plan(type=type, interval=interval, amount_per_month=amount_per_month)

    def __set_up_plan(self, type='type', interval='monthly', amount_per_month=5):
        plan = self.__mkPlan(type, interval, amount_per_month)
        self.sut.service.getPlanByTypeAndInterval.return_value = plan
        return self.sut.getPlanByTypeAndInterval(type=type, interval=interval)
