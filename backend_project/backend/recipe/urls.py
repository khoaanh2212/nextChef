from django.conf.urls import patterns, url

from .api import PhotoChangeOrderView
from .api import PhotoChangeCoverView
from .api import PhotoChangeInstructionsView
from .api import PhotoUploadView
from .api import RecipeChangeNameView
from .api import RecipeEditIngredientView
from .api import RecipeMakePublicView
from .api import RecipeMakePrivateView
from .api import PhotoDeleteView
from .api import CommentRecipeView
from .api import AddBookWithRecipeView
from .api import LoveView
from .api import RecipeChangePricingView

urlpatterns = patterns('',
                       url(r'create/?$', 'recipe.views.create_recipe', name='create-recipe'),
                       url(r'^detail/(?P<id>[^/]*)$', 'recipe.views.recipe', {'slug': ''}, name='recipe'),
                       url(r'^delete/(?P<id>[^/]*)$', 'recipe.views.delete', name='delete-recipe'),
                       url(r'^love/(?P<recipe_id>[^/]*)/?$', LoveView.as_view(), name='recipe_love'),
                       url(r'^edit/make-public/(?P<recipe_id>[^/]*)/?$', RecipeMakePublicView.as_view(), name='recipe-make-public'),
                       url(r'^edit/make-private/(?P<recipe_id>[^/]*)/?$', RecipeMakePrivateView.as_view(), name='recipe-make-private'),
                       url(r'^edit/name/(?P<recipe_id>[^/]*)/?$', RecipeChangeNameView.as_view(), name='recipe-edit-name'),
                       url(r'^edit/pricing/(?P<recipe_id>[^/]*)/?$',RecipeChangePricingView.as_view(),name='recipe-edit-pricing'),
                       url(r'^edit/ingredient/(?P<recipe_id>[^/]*)/?$', RecipeEditIngredientView.as_view(), name='recipe-edit-ingredient'),
                       url(r'^edit/photo/delete/(?P<photo_id>[^/]*)/?$', PhotoDeleteView.as_view(), name='recipe-delete-photo'),
                       url(r'^edit/photo/order/(?P<photo_id>[^/]*)/?$', PhotoChangeOrderView.as_view(), name='recipe-edit-photo-order'),
                       url(r'^edit/photo/instructions/(?P<photo_id>[^/]*)/?$', PhotoChangeInstructionsView.as_view(), name='recipe-edit-photo-instructions'),
                       url(r'^edit/photo/cover/(?P<photo_id>[^/]*)/?$', PhotoChangeCoverView.as_view(), name='recipe-edit-photo-cover'),
                       url(r'^add/photo/(?P<recipe_id>[^/]*)/?$', PhotoUploadView.as_view(), name='recipe-add-photo'),
                       url(r'^add/comment/(?P<recipe_id>[^/]*)/?$', CommentRecipeView.as_view(), name='comment-recipe'),
                       url(r'^add/book-with-recipe/(?P<recipe_id>[^/]*)/?$', AddBookWithRecipeView.as_view(), name='add-book-with-recipe'),
                       url(r'^(?P<slug>[^/]*)-(?P<id>[^/]*)$', 'recipe.views.recipe', name='recipe'),
                       url(r'^pdf/(?P<slug>[^/]*)-(?P<id>[^/]*)', 'recipe.views.recipe_pdf', name='recipe_download_pdf'),
                       #url(r'^pdf/(?P<id>[^/]*)', 'recipe.views.recipeView', name='pdf-recipe'),
                       #url(r'^change/photo/order/(?P<id>[^/]*)/?$', 'recipe.views.change_recipe_photo_order', name='change-recipe-photo-order'),
                       )
