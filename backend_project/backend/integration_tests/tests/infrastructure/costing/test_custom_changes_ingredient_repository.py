from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from infrastructure.costing.custom_changes_ingredient.CustomChangesIngredientRepository import CustomChangesIngredientRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.CustomChangesIngredientDataProvider import CustomChangesIngredientDataProvider


class CustomChangesIngredientRepositoryTest(IntegrationTestCase):

    def setUp(self):
        super(CustomChangesIngredientRepositoryTest, self).setUp()
        self.sut = CustomChangesIngredientRepository.new()

    def test_save_should_saveTheInstance(self):
        ingredient = CustomChangesIngredientDataProvider.get().with_ingredient('A').build()
        self.sut.save(ingredient)
        ingredients = self.sut.model.objects.filter(ingredient='A')
        self.assertTrue(len(ingredients) > 0)

    def test_remove_should_throw_whenIdInvalid(self):
        self.assertRaises(CustomChangesIngredient.DoesNotExist, self.sut.remove, -1)
