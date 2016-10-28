import unittest
from test_data_provider.PlanDataProvider import PlanDataProvider
from domain.stripe.StripePlan import StripePlan as sut
from domain.InvalidArgumentException import InvalidDomainArgumentException

class StripePlanTest(unittest.TestCase):
    '''
        StripePlan test
    '''

    def setUp(self):
        self.plan = PlanDataProvider.getDefault()

    def test_constructor_should_throw_if_not_provide_a_Plan_object(self):
        self.assertRaises(InvalidDomainArgumentException, sut.new, '')

    def test_constructor_should_not_throw_if_provide_a_Plan_object(self):
        sut.new(self.plan)
        self.assert_(True)

    def test_plan_id_is_calculated_correctly(self):
        plan = PlanDataProvider.get().withType('test type').withInterval('interval').build()
        actual = sut.new(plan)
        self.assertEqual(actual.id, 'test_type__interval')

    def test_plan_amount_is_selected_correctly_monthly(self):
        plan = PlanDataProvider.get().withInterval('monthly').withAmountPerMonth(1).withAmountPerYear(12).build()
        actual = sut.new(plan)
        self.assertEqual(actual.amount, 100)

    def test_plan_amount_is_selected_correctly_annually(self):
        plan = PlanDataProvider.get().withInterval('annually').withAmountPerMonth(1).withAmountPerYear(12).build()
        actual = sut.new(plan)
        self.assertEqual(actual.amount, 1200)

    def test_plan_interval_is_translated_correctly_monthly(self):
        plan = PlanDataProvider.get().withInterval('monthly').build()
        actual = sut.new(plan)
        self.assertEqual(actual.interval, 'month')

    def test_plan_interval_is_translated_correctly_annually(self):
        plan = PlanDataProvider.get().withInterval('annually').build()
        actual = sut.new(plan)
        self.assertEqual(actual.interval, 'year')
