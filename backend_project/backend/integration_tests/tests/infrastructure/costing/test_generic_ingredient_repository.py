from domain.costing.generic_ingredient.GenericIngredient import GenericIngredient
from infrastructure.costing.generic_ingredient.GenericIngredientRepository import GenericIngredientRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.GenericIngredientDataProvider import GenericIngredientDataProvider


class GenericIngredientRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(GenericIngredientRepositoryTest, self).setUp()
        self.sut = GenericIngredientRepository.new()
        self.instances = self.exerciseSave()

    def test_findAll_should_returnAllCosting(self):
        actual = self.sut.findAll()
        self.assertEqual(len(actual), len(self.instances))

    def test_findAll_should_filter(self):
        actual = self.sut.findAll(filter='celery')
        self.assertEqual(list(actual), [self.instances[0]])

    def test_findAll_should_doPagination_firstCase(self):
        actual = self.sut.findAll(page=1, limit=3)
        self.assertEqual(list(actual), [self.instances[0], self.instances[3], self.instances[1]])

    def test_findAll_should_doPagination_secondCase(self):
        actual = self.sut.findAll(page=2, limit=2)
        self.assertEqual(list(actual), [self.instances[1], self.instances[2]])

    def test_findById_should_throw_whenIdInvalid(self):
        self.assertRaises(GenericIngredient.DoesNotExist, self.sut.findById, -1)

    def exerciseSave(self):
        instances = self._mkDefaultCosting()
        self._save(instances)
        return instances

    def _save(self, instances):
        for ins in instances:
            ins.save()

    def _mkDefaultCosting(self):
        return [
            GenericIngredientDataProvider.get().withIngredient('Celery').build(),
            GenericIngredientDataProvider.get().withIngredient('Salmon').build(),
            GenericIngredientDataProvider.get().withIngredient('Sugar').build(),
            GenericIngredientDataProvider.get().withIngredient('Rice').build(),
        ]

    def tearDown(self):
        ids = map(lambda x: x.id, self.instances)
        self.sut.model.objects.filter(id__in=ids).delete()
