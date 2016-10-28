# -*- coding: utf-8 -*-
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

from django.core.management.base import BaseCommand

from recipe.models import Recipes


class Command(BaseCommand):
    help = 'Try to detect language of a recipe'
    languages = {
        u'danish': 'da',
        u'dutch': 'nl',
        u'english': 'en',
        u'finnish': 'fi',
        u'french': 'fr',
        u'german': 'de',
        u'hungarian': 'hu',
        u'italian': 'it',
        u'norwegian': 'nn',
        u'portuguese': 'pt',
        u'russian': 'ru',
        u'spanish': 'es',
        u'swedish': 'sv',
        u'turkish': 'tr'
    }

    def handle(self, *args, **options):
        recipes = Recipes.objects.filter(draft=False, language__isnull=True)

        k = 0

        for recipe in recipes:
            language_code = ''
            try:
                # Recipe text based on title, ingredients and steps
                recipe_text = recipe.name
                for ingredient in recipe.ingredients.all():
                    recipe_text = recipe_text + " " + ingredient.name
                for photo in recipe.photos.filter(chef__isnull=True).exclude(instructions=''):
                    recipe_text = recipe_text + " " + photo.instructions

                if len(recipe_text) <= 100:
                    language_code = 'short'
                else:
                    recipe_text = recipe_text.replace('\n', ' ')
                    language = self.detect_language(recipe_text)
                    language_code = self.languages.get(language, 'unkw')
            except Exception, e:
                self.stdout.write("Error %s processing recipe (%s) - %s" % (e, recipe.id, recipe.name))
                language_code = 'error'

            recipe.language = language_code
            recipe.save()
            k += 1

        self.stdout.write("%s Recipes processed" % k)

    def _calculate_languages_ratios(self, text):
        """
        Calculate probability of given text to be written in several languages and
        return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

        @param text: Text whose language want to be detected
        @type text: str

        @return: Dictionary with languages and unique stopwords seen in analyzed text
        @rtype: dict
        """
        languages_ratios = {}

        tokens = wordpunct_tokenize(text.lower())
        words = [word for word in tokens]

        # Compute per language included in nltk number of unique stopwords appearing in analyzed text
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)

            languages_ratios[language] = len(common_elements)  # language "score"

        return languages_ratios

    def detect_language(self, text):
        """
        Calculate probability of given text to be written in several languages and
        return the highest scored.

        It uses a stopwords based approach, counting how many unique stopwords
        are seen in analyzed text.

        @param text: Text whose language want to be detected
        @type text: str

        @return: Most scored language guessed
        @rtype: str
        """
        ratios = self._calculate_languages_ratios(text)

        most_rated_language = max(ratios, key=ratios.get)

        return most_rated_language
