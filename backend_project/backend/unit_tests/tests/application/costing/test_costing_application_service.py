import unittest, mock
from application.costing.CostingApplicationService import CostingApplicationService
from test_data_provider.GenericIngredientDataProvider import GenericIngredientDataProvider


class CostingApplicationServiceTest(unittest.TestCase):

    def setUp(self):
        self.costingServiceStub = mock.Mock()
        self.custom_changes_ingredient_stub = mock.Mock()
        self.costing_ingredient_service_stub = mock.Mock()
        self.sut = CostingApplicationService.new(
            generic_ingredient_service=self.costingServiceStub,
            custom_changes_ingredient_service=self.custom_changes_ingredient_stub,
            costing_ingredient_service=self.costing_ingredient_service_stub
        )

    def test_getCostingTable_should_returnDTOs(self):
        self.costing_ingredient_service_stub.get_costing_table.return_value = self._mkCostingList()
        actual = self.sut.get_costing_table('')
        expected = [
            {
                'id': None,
                'ingredient': 'Apple', 'family': 'Fruit', 'supplier': 'FarmerMarket',
                'quantity' : 1, 'unit': 'kg'
            },
            {
                'id': None,
                'ingredient': 'Salmon', 'family': 'Fish', 'supplier': 'SuperMarket',
                'quantity' : 1, 'unit': 'kg'
            },
            {
                'id': None,
                'ingredient': 'Milk', 'family': 'Dairy', 'supplier': 'HomeMade',
                'quantity' : 1, 'unit': 'kg'
            }
        ]
        self.assertEqual(actual, expected)

    def test_remove_custom_ingredient_row_should_removeTheIngredient(self):
        self.sut.remove_custom_ingredient_row(10)
        self.custom_changes_ingredient_stub.remove_custom_ingredient.assert_called_with(10)

    def test_remove_custom_generic_ingredient_row_should_call_remove_custom_generic_ingredient(self):
        self.costingServiceStub.get_by_id.return_value = {}
        self.sut.remove_custom_generic_ingredient_row('chef', 'id')
        self.costingServiceStub.get_by_id.assert_called_with('id')
        self.custom_changes_ingredient_stub.remove_custom_generic_ingredient.assert_called_with('chef', {})

    def _mkCostingList(self):
        return [
            GenericIngredientDataProvider.get().withIngredient('Apple').withFamily('Fruit').withSupplier('FarmerMarket').build(),
            GenericIngredientDataProvider.get().withIngredient('Salmon').withFamily('Fish').withSupplier('SuperMarket').build(),
            GenericIngredientDataProvider.get().withIngredient('Milk').withFamily('Dairy').withSupplier('HomeMade').build(),
        ]

    def test_get_recipe_suggestion_list_should_returnExpected(self):
        self.costing_ingredient_service_stub.get_suggestion_list.return_value = []
        self.costing_ingredient_service_stub.count_suggestion_list.return_value = 100
        actual = self.sut.get_ingredient_suggestion_list('', '', 4)
        expected = {
            "has_more": True,
            "total": 100,
            "list": []
        }
        self.assertEqual(actual, expected)
