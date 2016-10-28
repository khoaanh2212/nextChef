import unittest

from domain.costing.custom_changes_ingredient.CustomChangesIngredient import CustomChangesIngredient
from domain.costing.custom_changes_ingredient.CustomChangesIngredient import InvalidChef, InvalidIngredient
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.CostingIngredientDataProvider import CostingIngredientDataProvider
from test_data_provider.GenericIngredientDataProvider import GenericIngredientDataProvider


class CustomChangesIngredientTest(unittest.TestCase):

    def setUp(self):
        self.chef = ChefDataProvider.get().withId(1).build()
        self.ingredient = CostingIngredientDataProvider.get_default()
        self.generic_ingredient = GenericIngredientDataProvider.getDefault()
        self.sut = CustomChangesIngredient

    def test_create_should_throw_whenInvalidChef(self):
        self.assertRaises(InvalidChef, self.sut.create, {}, self.ingredient)

    def test_create_should_throw_whenInvalidGenericIngredient(self):
        self.assertRaises(InvalidIngredient, self.sut.create, self.chef, {})

    def test_create_should_not_throw_whenValid(self):
        self.sut.create(self.chef, self.ingredient)
        self.assert_(True)

    def test_create_should_returnCustomChangesIngredientInstance_whenValid(self):
        actual = self.sut.create(self.chef, self.ingredient)
        self.assertTrue(isinstance(actual, CustomChangesIngredient))

    def test_remove_should_throw_whenInputInvalid(self):
        test_cases = [
            {'chef': self.chef, 'ingredient': {}, 'exception': InvalidIngredient},
            {'chef': self.chef, 'ingredient': self.ingredient, 'exception': InvalidIngredient},
            {'chef': {}, 'ingredient': self.generic_ingredient, 'exception': InvalidChef},
        ]

        for test_case in test_cases:
            self.assertRaises(test_case['exception'], self.sut.remove, test_case['chef'], test_case['ingredient'])

    def test_remove_should_notThrow_whenInputValid(self):
        self.sut.remove(self.chef, self.generic_ingredient)
        self.assert_(True)

    def test_remove_should_returnExpected_whenInputValid(self):
        actual = self.sut.remove(self.chef, self.generic_ingredient)
        self.assertTrue(isinstance(actual, CustomChangesIngredient))
        self.assertEqual(actual.is_deleted, True)
