# -*- coding: utf-8 -*-
from __future__ import division
from datetime import timedelta

from django.utils.timezone import now
from django.db.models import Count, Q
from django.core.management.base import BaseCommand

from recipe.models import Recipes, Likes, ChefsHasRecipes


class Command(BaseCommand):
    help = 'Calculates recipe order rank'

    # Parameters need refactoring for user editing in backend
    DAYS_CONSIDERED_NEW = 7.0
    NEW_COEFICIENT = 35.0
    LIKES_COEFICIENT = 15.0
    PHOTOS_COEFICIENT = 20.0
    PHOTOS_WITH_DESCRIPTION_COEFICIENT = 20.0
    ADDED_COEFICIENT = 10.0
    NEW_FACTOR = NEW_COEFICIENT / DAYS_CONSIDERED_NEW
    REGULAR_NUM_PHOTOS = 8.0
    GRAVITY_FACTOR = 0.8

    # MAX Values from database
    max_likes = 0
    max_added = 0

    def handle(self, *args, **options):
        today = now()

        # Get max number of likes to a Recipe
        self.max_likes = self._get_max_likes()
        self.stdout.write("Max likes:\t%s" % self.max_likes)

        # Get max times added
        self.max_added = self._get_max_added()
        self.stdout.write("Max Added:\t%s" % self.max_added)

        # Reset score for draft and private recipes
        Recipes.objects.filter(Q(draft=True) | Q(private=True)).update(final_score=0)

        # Process all active recipes
        k = 0
        recipes = Recipes.objects.filter(draft=False, private=False)
        for recipe in recipes:
            # New factor
            recipe_new_until = recipe.creation_date + timedelta(self.DAYS_CONSIDERED_NEW, 0)
            if recipe_new_until > today:
                delta = recipe_new_until - today
                days = delta.days
                new_score = days * self.NEW_FACTOR
            else:
                new_score = 0.0

            # Likes
            num_likes = recipe.likes.count()
            likes_score = float(num_likes) / self.max_likes

            # Added
            num_added = recipe.chefshasrecipes_set.count()
            added_score = float(num_added) / self.max_added

            # Number of photos
            num_photos = recipe.photos.count()
            if num_photos > self.REGULAR_NUM_PHOTOS:
                photos_score = 1.0
            else:
                photos_score = num_photos / self.REGULAR_NUM_PHOTOS

            # Number of photos with description
            num_photos_with_instructions = recipe.photos.exclude(instructions__isnull=True)\
                                                        .exclude(instructions='').count()
            if num_photos_with_instructions == 0 or num_photos == 0:
                photos_with_instructions_score = 0.0
            else:
                photos_with_instructions_score = float(num_photos_with_instructions) / num_photos

            # Gravity Factor
            age_delta = today - recipe.creation_date
            recipe_age = age_delta.days + 1
            recipe_gravity = pow(recipe_age, self.GRAVITY_FACTOR)

            # score calculation
            cache_score = new_score \
                + likes_score * self.LIKES_COEFICIENT \
                + photos_score * self.PHOTOS_COEFICIENT \
                + photos_with_instructions_score * self.PHOTOS_WITH_DESCRIPTION_COEFICIENT \
                + added_score * self.ADDED_COEFICIENT \

            # score adjusted to time
            cache_score /= recipe_gravity

            # Manual score
            final_score = recipe.manual_score if recipe.manual_score > 0.0 else cache_score

            # Update recipe scores and cache counters
            k += 1
             
            recipe.cache_novelty_score = new_score
            recipe.cache_likes = num_likes
            recipe.cache_likes_score = likes_score
            recipe.cache_added = num_added
            recipe.cache_added_score = added_score
            recipe.cache_photos = num_photos
            recipe.cache_photos_score = photos_score
            recipe.cache_photo_descriptions = num_photos_with_instructions
            recipe.cache_photo_descriptions_score = photos_with_instructions_score
            recipe.cache_score = cache_score
            recipe.final_score = final_score
            # Update old fields for compatibility versions
            recipe.nb_added = num_added
            recipe.nb_likes = num_likes
            #recipe.nb_shares = 
            #recipe.nb_comments = 
            
            recipe.save()

        self.stdout.write("Recipes processed:\t%s" % k)


    @staticmethod
    def _get_max_likes():
        # Get max number of likes to a Recipe
        likes = Likes.objects.all().values('recipe').annotate(total=Count('recipe')).order_by('-total')[:1]

        if likes:
            l = likes[0]
            return l['total']

        return 0

    @staticmethod
    def _get_max_added():
        adds = ChefsHasRecipes.objects.all().values('recipe').annotate(total=Count('recipe')).order_by('-total')[:1]
        if adds:
            a = adds[0]
            return a['total']

        return 0