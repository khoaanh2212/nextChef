from django.conf.urls import patterns, include, url

from . import api


urlpatterns = patterns(
    '',
    # Ingredients
    url(r'^recipes/(?P<recipe_pk>\d+)/ingredients$', api.IngredientView.as_view()),
    url(r'^recipes/(?P<recipe_pk>\d+)/ingredients/(?P<pk>\d+)$', api.IngredientView.as_view()),
    # New Ingredient API
    url(r'^recipes/(?P<recipe_pk>\d+)/ingredient$', api.RecipeIngredientView.as_view()),

    url(r'^ingredients$', api.IngredientListView.as_view()),

    # Tags
    url(r'^recipes/(?P<recipe_pk>\d+)/tags$', api.TagView.as_view()),
    url(r'^recipes/(?P<recipe_pk>\d+)/tags/(?P<pk>\d+)$', api.TagView.as_view()),

    # Photos
    url(r'^recipes/(?P<recipe_pk>\d+)/photos$', api.PhotoView.as_view()),
    url(r'^recipes/(?P<recipe_pk>\d+)/photos/(?P<pk>\d+)$', api.PhotoView.as_view()),
    url(r'^updated/photos$', api.UpdatedPhotosView.as_view()),
    # Styles
    url(r'^styles/(?P<action>photos(|_url))/(?P<pk>\d+)/(?P<filter>\w+)$', api.StyleView.as_view()),

    # Books
    url(r'^recipes/(?P<recipe_pk>\d+)/books$', api.BookView.as_view()),

    # Comments
    url(r'^recipes/(?P<recipe_pk>\d+)/comments$', api.CommentView.as_view()),
    # Likes
    url(r'^recipes/(?P<recipe_pk>\d+)/likes$', api.LikeView.as_view()),
    # Reports
    url(r'^recipes/(?P<recipe_pk>\d+)/report$', api.ReportView.as_view()),
    # Shares
    url(r'^recipes/(?P<recipe_pk>\d+)/shares$', api.ShareView.as_view()),

    # Recipes
    url(r'^recipes$', api.RecipeView.as_view()),
    url(r'^recipes/(?P<pk>\d+)$', api.RecipeView.as_view()),
    # Recipes searchs
    url(r'^(?P<action>explore)/new$', api.RecipeSearchView.as_view()),
    url(r'^(?P<action>new)/recipes$', api.RecipeSearchView.as_view()),
    url(r'^(?P<action>updated)/recipes$', api.RecipeSearchView.as_view()),
    url(r'^(?P<action>search)$', api.RecipeSearchView.as_view()),

    # SubRecipe Search
    url(r'^subrecipes$', api.SubRecipeView.as_view()),

    # Recipe Details
    url(r'^recipes/(?P<pk>\d+)/details$', api.RecipeDetailView.as_view()),

    # Allergens
    url(r'^recipes/(?P<pk>\d+)/allergens$', api.AllergenView.as_view()),

    url(r'^recipes/edamam$', api.EdamamView.as_view(), name='edamam'),
)
