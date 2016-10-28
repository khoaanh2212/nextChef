from integration_tests.api_test_case import ApiTestCase
from recipe.models import Recipes, Ingredients, RecipesHasIngredients


class RecipeTest(ApiTestCase):
    def test_sorted_ingredients(self):
        """
        Test ingredients sorting functions
        """
        ing1 = Ingredients.objects.create(name="Ingredient 1")
        ing2 = Ingredients.objects.create(name="Ingredient 2")
        ing3 = Ingredients.objects.create(name="Ingredient 3")

        r = Recipes()

        r.set_ingredients_order([ing2, ing1])
        self.assertEqual(r.ingredients_order, "a:2:{i:0;i:%i;i:1;i:%i;}" % (ing2.pk, ing1.pk))

        r.set_ingredients_order_delete(ing2)
        self.assertEqual(r.ingredients_order, "a:1:{i:0;i:%i;}" % (ing1.pk))

        r.set_ingredients_order_add(ing2)
        self.assertEqual(r.ingredients_order, "a:2:{i:0;i:%i;i:1;i:%i;}" % (ing1.pk, ing2.pk))

        r.set_ingredients_order([ing2, ing1, ing3])
        r.save()
        for i in ing1, ing2, ing3:
            RecipesHasIngredients.objects.create(recipe=r, ingredient=i)
        self.assertEqual(r.get_sorted_ingredients(), [ing2, ing1, ing3])
