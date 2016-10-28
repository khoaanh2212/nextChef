import unittest
from domain.recipe.RecipeHasSubrecipe import RecipeHasSubrecipe, InvalidRecipeHasSubrecipeArgumentException
from domain.PositiveFloatNumber import InvalidFloatNumberException
from test_data_provider.RecipeDataProvider import RecipeDataProvider
from test_data_provider.ChefDataProvider import ChefDataProvider
from domain.recipe.SelectedAllergens import SelectedAllergens


class RecipeHasSubrecipeTest(unittest.TestCase):
    def setUp(self):
        self.sut = RecipeHasSubrecipe
        self.recipe1 = RecipeDataProvider.get().with_id(1).build()
        self.recipe2 = RecipeDataProvider.get().with_id(2).with_allergens('allergens').build()
        self.recipe2.chef = ChefDataProvider.getDefault()
        self.order = 0

    def test_create_should_throw_whenInputInvalid(self):
        test_cases = [
            {'recipe': '', 'sub_recipe': '', 'sub_recipe_price': 50,
             'exception': InvalidRecipeHasSubrecipeArgumentException},
            {'recipe': {}, 'sub_recipe': self.recipe1, 'sub_recipe_price': 50,
             'exception': InvalidRecipeHasSubrecipeArgumentException},
            {'recipe': self.recipe1, 'sub_recipe': self.recipe1, 'sub_recipe_price': 50,
             'exception': InvalidRecipeHasSubrecipeArgumentException},
            {'recipe': self.recipe1, 'sub_recipe': self.recipe2, 'sub_recipe_price': 'invalid',
             'exception': InvalidFloatNumberException},
            {'recipe': self.recipe1, 'sub_recipe': self.recipe2, 'sub_recipe_price': -10,
             'exception': InvalidFloatNumberException}
        ]
        for test_case in test_cases:
            self.assertRaises(test_case['exception'], self.sut.create, test_case['recipe'], test_case['sub_recipe'],
                              test_case['sub_recipe_price'], SelectedAllergens([]), self.order, '')

    def test_create_should_notThrow_whenInputValid(self):
        self.sut.create(self.recipe1, self.recipe2, 50, SelectedAllergens([]), self.order, '')
        self.assert_(True)

    def test_create_should_returnExpected(self):
        actual = self.sut.create(self.recipe1, self.recipe2, 50, SelectedAllergens(['Fish']), self.order, '')
        self.assertTrue(isinstance(actual, RecipeHasSubrecipe))
        self.assertEqual(actual.r_id, 1)
        self.assertEqual(actual.sr_id, 2)
        self.assertEqual(actual.sr_price, 50)
        self.assertEqual(actual.sr_allergens, 'Fish')
