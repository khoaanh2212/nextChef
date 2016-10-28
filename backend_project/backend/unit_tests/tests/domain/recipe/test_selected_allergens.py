from domain.recipe.SelectedAllergens import SelectedAllergens, InvalidAllergen, Allergen, ALLERGEN_TITLES
import unittest
from mock import Mock


class SelectedAllergensTest(unittest.TestCase):
    sut = SelectedAllergens

    def test_new_whenReceiveBadAllergen_throwsInvalidAllergen(self):
        self.assertRaises(InvalidAllergen, self.sut.new, 'something')

    def test_new_whenReceiveOneGoodAllergen_returnsThatAllergen(self):
        expected = ["Celery"]
        actual = self.sut.new(expected).__str__()
        self.assertEqual(actual, "Celery")

    def test_add_whenReceiveOneGoodAllergenOnEmptySelection_returnsThatAllergen(self):
        expected = "Celery"
        sut = self.empty_allergens()
        sut.add(Allergen(expected))
        self.assertEqual(sut.__str__(), expected)

    def test_new_whenNoParameter_returnsNoAllergens(self):
        self.assertEqual(self.sut.new().__str__(), "")

    def empty_allergens(self):
        return self.sut.new()

    def test_add_whenAddMoreThanOneAllergen_returnExpected(self):
        expected = "Celery, Nuts"
        sut = self.empty_allergens()
        sut.add(Allergen("Celery"))
        sut.add(Allergen("Nuts"))
        self.assertEqual(sut.__str__(), expected)

    def test_remove_whenGiveAnExistAllergen_shouldRemoveFromList(self):
        example_list = ["Celery", "Nuts", "Milk"]
        sut = self.sut.new(example_list)
        sut.remove(Allergen("Celery"))
        self.assertEqual(sut.allergens.__len__(), 2)

    def test_add_WhenAddAnExistAllergen_ReturnSameList(self):
        sut = self.sut.new(["Celery", "Nuts", "Eggs"])
        sut.add(Allergen("Celery"))
        self.assertEqual(sut.allergens.__len__(), 3)
