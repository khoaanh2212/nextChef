from infrastructure.costing.CostingIngredientViewRepository import CostingIngredientViewRepository
from integration_tests.integration_test_case import IntegrationTestCase
from test_data_provider.ChefDataProvider import ChefDataProvider
from test_data_provider.CustomChangesIngredientDataProvider import CustomChangesIngredientDataProvider
from test_data_provider.GenericIngredientDataProvider import GenericIngredientDataProvider


class CostingIngredientViewRepositoryTest(IntegrationTestCase):
    def setUp(self):
        super(CostingIngredientViewRepositoryTest, self).setUp()
        self.sut = CostingIngredientViewRepository.new()
        self.test_data = self.exercise_create_test_data()

    def test_get_by_chef_id_should_returnExpected_caseChef1(self):
        actual = self.sut.find_by_chef_id(self.test_data['chef'][0].id)
        actual = map(lambda x: x.to_dto(), list(actual))
        expected = self.exercise_get_expected_for_chef1(self.test_data)
        self.assertEqual(actual, expected)

    def test_get_by_chef_id_should_returnExpected_caseChef2(self):
        actual = self.sut.find_by_chef_id(self.test_data['chef'][1].id)
        actual = map(lambda x: x.to_dto(), list(actual))
        expected = self.exercise_get_expected_for_chef2(self.test_data)
        self.assertEqual(actual, expected)

    def test_get_by_chef_id_should_countCorrectly_caseChef2(self):
        actual = self.sut.count_by_chef_id(self.test_data['chef'][1].id)
        self.assertEqual(actual, 6)

    def test_get_by_chef_id_should_countCorrectly_caseChef2_whenFiltered(self):
        actual = self.sut.count_by_chef_id(self.test_data['chef'][1].id, '1')
        self.assertEqual(actual, 2)

    def makeResultItem(self, chef_id, custom_id, generic_id, ingredient, deleted):
        return {
            'chef_id': chef_id,
            'custom_id': custom_id,
            'generic_table_row_id': generic_id,
            'ingredient': ingredient,
            'family': '',
            'supplier': '',
            'quantity': 1,
            'unit': 'kg',
            'gross_price': None,
            'net_price': None,
            'waste': None
        }

    def exercise_get_expected_for_chef1(self, test_data):
        return [
            self.makeResultItem(None, None, test_data['generic_ingr'][0].id, 'ingr1', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][2].id, 'ingr3', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][3].id, 'ingr4', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][4].id, 'ingr5', None),
            self.makeResultItem(test_data['chef'][0].id, test_data['custom_ingr'][0].id, None, 'new_ingr1', None),
            self.makeResultItem(test_data['chef'][0].id, test_data['custom_ingr'][1].id, None, 'new_ingr2', None),
        ]

    def exercise_get_expected_for_chef2(self, test_data):
        return [
            self.makeResultItem(None, None, test_data['generic_ingr'][0].id, 'ingr1', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][1].id, 'ingr2', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][2].id, 'ingr3', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][3].id, 'ingr4', None),
            self.makeResultItem(None, None, test_data['generic_ingr'][4].id, 'ingr5', None),
            self.makeResultItem(test_data['chef'][1].id, test_data['custom_ingr'][3].id, None, 'new_ingr1', False),
        ]

    def exercise_create_test_data(self):
        chef1 = ChefDataProvider.get().withEmail('chef1@mail.com').build()
        chef2 = ChefDataProvider.get().withEmail('chef2@mail.com').build()
        self.save_instances([chef1, chef2])

        gen_ingr1 = GenericIngredientDataProvider.get().withIngredient('ingr1').build()
        gen_ingr2 = GenericIngredientDataProvider.get().withIngredient('ingr2').build()
        gen_ingr3 = GenericIngredientDataProvider.get().withIngredient('ingr3').build()
        gen_ingr4 = GenericIngredientDataProvider.get().withIngredient('ingr4').build()
        gen_ingr5 = GenericIngredientDataProvider.get().withIngredient('ingr5').build()
        self.save_instances([gen_ingr1, gen_ingr2, gen_ingr3, gen_ingr4, gen_ingr5])

        custom_ingr1 = CustomChangesIngredientDataProvider.get() \
            .with_chef_id(chef1.id) \
            .with_ingredient('new_ingr1') \
            .build()

        custom_ingr2 = CustomChangesIngredientDataProvider.get() \
            .with_chef_id(chef1.id) \
            .with_ingredient('new_ingr2') \
            .build()

        custom_ingr3 = CustomChangesIngredientDataProvider.get() \
            .with_chef_id(chef1.id) \
            .with_generic_ingredient_id(gen_ingr2.id) \
            .with_is_deleted(True) \
            .build()

        custom_ingr4 = CustomChangesIngredientDataProvider.get() \
            .with_chef_id(chef2.id) \
            .with_ingredient('new_ingr1') \
            .build()

        self.save_instances([custom_ingr1, custom_ingr2, custom_ingr3, custom_ingr4])

        return dict(
            custom_ingr=[custom_ingr1, custom_ingr2, custom_ingr3, custom_ingr4],
            generic_ingr=[gen_ingr1, gen_ingr2, gen_ingr3, gen_ingr4, gen_ingr5],
            chef=[chef1, chef2]
        )

    def save_instances(self, instances):
        for ins in instances:
            ins.save()
