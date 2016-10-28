import mock, unittest
from application.recipe.RecipeApplicationService import RecipeApplicationService
from test_data_provider.RecipeDataProvider import RecipeDataProvider
from test_data_provider.RecipeHasIngredientDataProvider import RecipeHasIngredientDataProvider
from test_data_provider.RecipeHasSubrecipeDataProvider import RecipeHasSubrecipeDataProvider
from legacy_wrapper.recipe_wrapper import Recipe
from domain.costing.CostingIngredient import CostingIngredient


class RecipeApplicationServiceTest(unittest.TestCase):
    def setUp(self):
        self.recipe_service_stub = mock.Mock()
        self.edamam_service_stub = mock.Mock()
        self.book_service_stub = mock.Mock()
        self.costing_ingredient_service_stub = mock.Mock()
        self.recipe_ingredient_service_stub = mock.Mock()
        self.recipe_subrecipe_service_stub = mock.Mock()
        self.recipe_wrapper_stub = mock.Mock()
        self.recipe_permission_view_repo_stub = mock.Mock()
        self.custom_changes_ingredient_service_stub = mock.Mock()

        self.sut = RecipeApplicationService.new(
            recipe_service=self.recipe_service_stub,
            edamam_service=self.edamam_service_stub,
            book_service=self.book_service_stub,
            custom_changes_ingredient_service=self.custom_changes_ingredient_service_stub,
            costing_ingredient_service=self.costing_ingredient_service_stub,
            recipe_ingredient_service=self.recipe_ingredient_service_stub,
            recipe_subrecipe_service=self.recipe_subrecipe_service_stub,
            recipe_wrapper=self.recipe_wrapper_stub,
            recipe_permission_view_repo=self.recipe_permission_view_repo_stub
        )

    def test_analyzeEdamam_should_returnAllergenList(self):
        self.edamam_service_stub.getAllergens.return_value = 'list-of-allergens'
        actual = self.sut.analyzeEdamam('')
        self.assertEqual(actual, 'list-of-allergens')

    def test_get_recipe_by_books_should_returnUniqueRecipes(self):
        recipe1 = RecipeDataProvider.get().with_id(1).build()
        recipe2 = RecipeDataProvider.get().with_id(2).build()
        recipe3 = RecipeDataProvider.get().with_id(1).build()
        self.book_service_stub.get_recipe_by_books.return_value = [recipe1, recipe2, recipe3]
        actual = self.sut.get_recipe_by_books('books')
        self.assertEqual(actual, [recipe1, recipe2])

    def test_get_recipe_in_public_books(self):
        recipe1 = RecipeDataProvider.get().with_id(1).build()
        recipe2 = RecipeDataProvider.get().with_id(2).build()
        self.book_service_stub.get_recipe_in_public_books.return_value = [recipe1, recipe2]
        recipe = self.recipe_wrapper_stub.return_value = mock.MagicMock()
        recipe.toDTO = mock.MagicMock()
        recipe.toDTO.return_value = {}
        actual = self.sut.get_recipe_in_public_books()
        expected = [{}, {}]
        self.assertEqual(actual, expected)

    def test_get_recipe_by_following_chef(self):
        recipe1 = RecipeDataProvider.get().with_id(1).build()
        recipe2 = RecipeDataProvider.get().with_id(2).build()
        self.book_service_stub.get_recipe_by_following_chef.return_value = [recipe1, recipe2]
        recipe = self.recipe_wrapper_stub.return_value = mock.MagicMock()
        recipe.toDTO = mock.MagicMock()
        recipe.toDTO.return_value = {}
        chef = mock.Mock()
        actual = self.sut.get_recipe_by_following_chef(chef)
        expected = [{}, {}]
        self.assertEqual(actual, expected)

    def test_getPriceAndAllergen_shouldServiceMethod(self):
        costing_method = self.sut.costing_ingredient_service.get_by_recipe_id = mock.MagicMock()
        recipe_method = self.sut.recipe_service.get_by_id = mock.MagicMock()
        recipe = mock.Mock()
        recipe.id = 1
        self.sut.get_price_and_allergen(recipe)
        self.assertTrue(costing_method.called)
        self.assertTrue(recipe_method.called)

    def test_getPriceAndAllergen_returnExpectedData(self):
        recipe = mock.Mock()
        costing_return = mock.Mock()
        recipe_return = mock.Mock()
        costing_return.gross_price = 'price'
        recipe_return.allergens = 'allergens'
        expected = {
            'price': 'price',
            'allergens': 'allergens'
        }

        costing_method = self.sut.costing_ingredient_service.get_by_recipe_id = mock.MagicMock()
        recipe_method = self.sut.recipe_service.get_by_id = mock.MagicMock()
        costing_method.return_value = costing_return
        recipe_method.return_value = recipe_return
        actual = self.sut.get_price_and_allergen(recipe)
        self.assertEqual(actual, expected)

    def test_get_allergens_for_recipe_should_returnExpected(self):
        ingr1 = RecipeHasIngredientDataProvider.get().with_allergens("allergen-1, allergen-2, allergen-3").build()
        ingr2 = RecipeHasIngredientDataProvider.get().with_allergens("allergen-1").build()
        reci1 = RecipeHasSubrecipeDataProvider.get().with_allergens("allergen-2, allergen-4").build()

        recipe = RecipeDataProvider.get().with_allergens("recipe-allergen").build()

        self.recipe_ingredient_service_stub.get_by_recipe_id.return_value = [ingr1, ingr2]
        self.recipe_subrecipe_service_stub.get_by_recipe_id.return_value = [reci1]
        self.recipe_service_stub.get_by_id.return_value = Recipe(recipe)

        actual = self.sut.get_allergens_for_recipe('')
        self.assertEqual(actual, ['allergen-1', 'allergen-2', 'allergen-3', 'allergen-4', 'recipe-allergen'])

    def test_add_subrecipe_should_forwardCorrectArguments(self):
        recipe = RecipeDataProvider.get_default()
        self.recipe_service_stub.get_by_id.return_value = Recipe(recipe)
        self.recipe_ingredient_service_stub.get_price.return_value = 10
        self.recipe_subrecipe_service_stub.get_price.return_value = 10
        self.sut.get_allergens_for_recipe = mock.Mock()
        self.sut.get_allergens_for_recipe.return_value = []
        self.sut.getBigestOrder = mock.Mock()
        self.sut.getBigestOrder.return_value = 1
        self.sut.add_subrecipe('', '', '')

        self.recipe_subrecipe_service_stub.create.assert_called_with(recipe, recipe, 20, [], 1, '')

    def test_get_recipe_suggestion_list_should_returnExpected(self):
        self.recipe_service_stub.get_suggestion_list.return_value = [
            RecipeHasSubrecipeDataProvider.get_default(),
            RecipeHasSubrecipeDataProvider.get_default()
        ]
        self.recipe_service_stub.count_suggestion_list.return_value = 100
        actual = self.sut.get_recipe_suggestion_list('', '', 4)
        expected = {
            "has_more": True,
            "total": 100,
            "list": [
                {
                    'allergens': '',
                    'recipe_id': None,
                    'subrecipe_id': 10,
                    'name': '',
                    'owner_name': '',
                    'price': 0,
                    'type': 'recipe',
                    'id': None,
                    'order': 0,
                    'amount': ''
                },
                {
                    'allergens': '',
                    'recipe_id': None,
                    'subrecipe_id': 10,
                    'name': '',
                    'owner_name': '',
                    'price': 0,
                    'type': 'recipe',
                    'id': None,
                    'order': 0,
                    'amount': ''
                }
            ]
        }
        self.assertEqual(actual, expected)

    def testGetBigestOrder_should_return_1_if_bigest_order_of_ingredient_is_zero_and_bigest_order_of_subRecipe_is_zero(
            self):
        recipeId = 1
        self.recipe_ingredient_service_stub.getBigestOrder.return_value = 0
        self.recipe_subrecipe_service_stub.getBigestOrder.return_value = 0
        actual = self.sut.getBigestOrder(recipeId)
        self.assertEqual(actual, 1)

    def testGetBigestOrder_should_return_bigestOrder_plus_1(self):
        recipeId = 1
        self.recipe_ingredient_service_stub.getBigestOrder.return_value = 1
        self.recipe_subrecipe_service_stub.getBigestOrder.return_value = 2
        actual = self.sut.getBigestOrder(recipeId)
        self.assertEqual(actual, 3)

    def test_get_all_public_recipe_should_return_public_recipe(self):
        self.recipe_permission_view_repo_stub.find_public_recipe.return_value = []
        self.recipe_service_stub.get_by_id.return_value = []
        actual = self.sut.get_all_public_recipes()
        self.recipe_service_stub.get_by_id.assert_called_with([])
        self.assertEqual(actual, [])

    def test_is_recipe_available_for_chef_should_returnTheResultFromRecipePermissionRepo(self):
        self.recipe_permission_view_repo_stub.is_recipe_available_for_chef.return_value = True
        actual = self.sut.is_recipe_available_for_chef(1, 1)
        self.assertTrue(actual)

    def test_add_new_ingredient_into_custom_ingredient_should_return_new_costing_ingredient(self):
        chef = mock.Mock()
        ingredientName = 'mango'
        self.custom_changes_ingredient_service_stub.add_custom_ingredient.return_value = {}
        actual = self.sut.add_new_ingredient_into_custom_ingredient(ingredientName, chef)
        self.assertEquals(actual, {})

    def test_handle_amount_ingredient_not_exists_should_return_1_if_first_word_not_a_number(self):
        actual = self.sut.handle_amout_ingredient(amount='hello guys')
        self.assertEquals(actual, '1')

    def test_handle_amount_ingredient_not_exists_should_return_number_if_first_word_is_a_number(self):
        actual = self.sut.handle_amout_ingredient(amount='10 persons')
        self.assertEquals(actual, '10')

    def test_RepresentFloat_should_return_false_if_string_is_not_number(self):
        actual = self.sut.RepresentFloat('whatever')
        self.assertEquals(actual, False)

    def test_RepresentFloat_should_return_true_if_string_is_a_number(self):
        actual = self.sut.RepresentFloat('1.00')
        self.assertEquals(actual, True)

    def test_handle_measure_ingredient_should_return_blank_if_string_has_less_two_words(self):
        actual = self.sut.hand_measure_ingredient('hey')
        self.assertEquals(actual,'')

    def test_hand_measure_ingredient_should_return_from_the_second_word_to_the_end_of_string_if_string_has_more_or_equal_two_words(self):
        actual = self.sut.hand_measure_ingredient('hey guys what ever')
        self.assertEquals(actual,'guys what ever')