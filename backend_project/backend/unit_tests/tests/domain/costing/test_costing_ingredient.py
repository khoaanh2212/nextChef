import unittest
from domain.costing.CostingIngredient import CostingIngredient, InvalidCostingIngredientArgumentException



class CostingIngredientTest(unittest.TestCase):

    def setUp(self):
        self.sut = CostingIngredient

    # ingredient, family, quantity, unit, gross_price, waste, net_price, supplier, comment
    def test_constructor_should_throwException_whenInputInvalid(self):
        self.assertRaises(InvalidCostingIngredientArgumentException, self.sut, 'ingr', 'fam', None, 'kg', '11.3', '-1', '15', 'sup', 'comment')

    def test_constructor_should_notThrow_whenInputValid(self):
        self.sut('ingredient')
        self.assert_(True)
