from domain.chefs.plan.Plan import Plan
from infrastructure.chefs.plan.PlanRepository import PlanRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.PlanDataProvider import PlanDataProvider


class PlanRepositoryTest(IntegrationTestCase):
    '''
        PlanRepositoryTest
    '''

    def setUp(self):
        super(PlanRepositoryTest, self).setUp()
        self.sut = PlanRepository()

    def test_insert_should_save_and_return_plan_object(self):
        plan = self._mkPlan()
        actual = self.sut.save(plan)
        pk = actual.pk
        saved_plan = Plan.objects.get(id=pk)
        self.assertIsNotNone(saved_plan)
        self.assertEqual(actual, plan)

    def test_findById_should_return_the_plan_object(self):
        self.sut.save(self._mkPlan())
        plan = Plan.objects.latest('id')
        plan_id = plan.id
        actual = self.sut.findById(plan_id)
        self.assertEqual(actual, plan)

    def _mkPlan(self):
        return PlanDataProvider.getDefault()
