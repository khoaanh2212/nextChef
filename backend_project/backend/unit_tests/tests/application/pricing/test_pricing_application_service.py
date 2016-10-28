# -*- coding: utf-8 -*-
import unittest
import mock

from application.pricing.PricingApplicationService import PricingApplicationService
from domain.pricing.PricingService import PricingService

class PricingServiceTest(unittest.TestCase):
    '''
        Pricing Service Unit Tests
    '''

    def setUp(self):
        self.sut = PricingApplicationService()

    def test_getFakeData_should_call_and_return_pricing_service_getFakeData(self):
        self.sut.pricing_service.getFakeData = mock.MagicMock(name='getFakeData')
        self.sut.pricing_service.getFakeData.return_value = []
        actual = self.sut.getFakeData()
        self.assertTrue(self.sut.pricing_service.getFakeData.called)
        self.assertEqual(actual, [])
