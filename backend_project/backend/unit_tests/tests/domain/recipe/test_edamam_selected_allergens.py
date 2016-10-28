from domain.recipe.SelectedAllergens import EdamamSelectedAllergens
import unittest


class EdamamSelectedAllergensTest(unittest.TestCase):
    def setUp(self):
        self.sut = EdamamSelectedAllergens

    def test_constructor_should_filterAllergens(self):
        edamam_allergens_free = [
            'GLUTEN_FREE', 'CRUSTACEAN_FREE', 'PEANUT_FREE', 'SOY_FREE', 'TREE_NUT_FREE', 'CELERY_FREE', 'MUSTARD_FREE',
            'SESAME_FREE', 'LUPINE_FREE', 'MOLLUSK_FREE'
        ]
        sut = self.sut.new(edamam_allergens_free)
        expected = [
            'Eggs', 'Fish', 'Milk'
        ]

        self.assertEqual(sut.selected_allergens, expected)
