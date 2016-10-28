# -*- coding: utf-8 -*-
from south.v2 import DataMigration

from domain.costing.generic_ingredient.GenericIngredientService import GenericIngredientService
from domain.costing.CostingIngredient import CostingIngredient
from random import randint
import logging
import os


class Migration(DataMigration):
    initial = True

    depends_on = (
        ('application', '0001_initial'),
        ('recipe', '0016_auto__add_recipehasingredient')
    )

    def forwards(self, orm):
        env_test_data = os.getenv('TEST_DATA', 'false')

        if not env_test_data == 'true':
            logging.info("Skipping TEST DATA")
            return

        generic_ingredient_service = GenericIngredientService.new()
        ingredients = ["Bacon","Beef fat","Butter","Chicken fat","Banana","Cocoa butter","Coconut or coconut oil","Lard","Apple","Peanut butter","Palm or palm kernel oil","Powdered whole milk solids","Shortening","Suet","Salmon","Tallow","Trans fat"	,"Hard margarine","Hydrogenated fats and oils","Partially hydrogenated fats and oils","Shortening","Sodium"	,"Baking powder","Baking soda","Brine","Peach","Celery salt","Disodium phosphate","Garlic salt","Monosodium glutamate","Onion salt","Salt","Melon","Soy sauce","Sugar"	,"Brown sugar","Cane juice extract","Corn syrup","Demerara or Turbinado sugar","Dextrose","Evaporated cane juice","Fructose","Galactose","Glucose","Glucose-fructose","High-fructose corn syrup","Honey","Invert sugar","Lactose","Liquid sugar","Maltose","Molasses","Sucrose","Syrup","Treacle"]
        for i in ingredients:
            ingredient = i
            quantity = randint(1, 10)
            ingredient = CostingIngredient(ingredient, quantity=quantity)
            generic_ingredient_service.add_ingredient(ingredient)


    def backwards(self, orm):
        pass

    complete_apps = ['costing']
