from django.conf.urls import patterns, url
from .api import RecipeSearchView as RecipeSearchViewV0
from .api_v1 import RecipesListView, RecipeRecommendedView

urlpatterns = patterns(
    '',
    url(r'^recipes/list/followings/?$', RecipesListView.as_view(), kwargs=dict(type='followings'),
        name='recipes-followings-list'),
    url(r'^recipes/list/recipes/?$', RecipesListView.as_view(), kwargs=dict(type='all'), name='recipes-list'),
    url(r'^recipes/list/recipes/pro/?$', RecipesListView.as_view(), kwargs=dict(type='pro'), name='recipes-pro-list'),
    url(r'^recipes/list/recipes/foodie/?$', RecipesListView.as_view(), kwargs=dict(type='foodie'), name='recipes-foodie-list'),

    # Search
    url(r'^(?P<action>recommended)$', RecipeRecommendedView.as_view()),
    url(r'^(?P<action>explore)$', RecipeSearchViewV0.as_view()),
    url(r'^(?P<action>updated)$', RecipeSearchViewV0.as_view()),
    url(r'^(?P<action>search)$', RecipeSearchViewV0.as_view()),
)
