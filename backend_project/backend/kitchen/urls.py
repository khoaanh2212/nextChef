from django.conf.urls import patterns, url


from .api import (RecipeView, 
                  UploadPhotoView,
                  PhotoDeleteView,
                  PhotoUpdateInstructionsView,
                  PhotoChangeOrderView,
                  EditIngredientsView,
                  EditTagsView,
                  EditTitleView,
                  EditCoverView,
                  SelectBookView,
                  ServesView,
                  PrepTimeView,
                  SuggestIngredientsView,)
from .views import add_allergen

urlpatterns = patterns('',
                       url(r'^/?$', 'kitchen.views.kitchen', name='kitchen'),
                       url(r'^draft/(?P<id>[^/]*)$', 'kitchen.views.draft', name='kitchen_draft'),
                       url(r'^publish/(?P<id>[^/]*)$', 'kitchen.views.publish', name='kitchen_publish'),
                       url(r'^make-private/(?P<id>[^/]*)$', 'kitchen.views.make_private', name='kitchen_make_private'),
                       url(r'^congratulations/(?P<id>[^/]*)$', 'kitchen.views.congratulations', name='kitchen_congratulations'),
                       url(r'^recipe/edit/(?P<id>[^/]*)$', 'kitchen.views.draft', name='kitchen_recipe'),
                       url(r'^recipe/get/(?P<id>[^/]*)$', RecipeView.as_view(), name='kitchen_get_recipe'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/upload/photo/$', UploadPhotoView.as_view(), name='kitchen_upload_photo'),
                       url(r'^recipe/delete/photo/(?P<photo_id>[^/]*)$', PhotoDeleteView.as_view(), name='kitchen_delete_photo'),
                       url(r'^recipe/edit/photo/(?P<photo_id>[^/]*)/instructions/$', PhotoUpdateInstructionsView.as_view(), name='kitchen_photo_update_instructions'),
                       url(r'^recipe/edit/photo/(?P<photo_id>[^/]*)/order/$', PhotoChangeOrderView.as_view(), name='kitchen_change_photo_order'),
                       url(r'^recipe/select/cover/(?P<photo_id>[^/]*)/$', EditCoverView.as_view(), name='kitchen_select_cover'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/ingredients/$', EditIngredientsView.as_view(), name='kitchen_edit_ingredients'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/tags/$', EditTagsView.as_view(), name='kitchen_edit_tags'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/title/$', EditTitleView.as_view(), name='kitchen_edit_title'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/serves/$', ServesView.as_view(), name='kitchen_edit_serves'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/prep-time/$', PrepTimeView.as_view(), name='kitchen_edit_prep_time'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/select/book/$', SelectBookView.as_view(), name='kitchen_select_book'),
                       #url(r'^recipe/(?P<recipe_id>[^/]*)/publish/$', PublishView.as_view(), name='kitchen_publish_recipe'),
                       #url(r'^recipe/(?P<recipe_id>[^/]*)/make-private/$', MakePrivateView.as_view(), name='kitchen_make_private_recipe'),
                       url(r'^ingredient/get/(?P<search_key>[^/]*)$', SuggestIngredientsView.as_view(), name='kitchen_suggestion_ingredients'),
                       url(r'^recipe/(?P<recipe_id>[^/]*)/edit/allergens/$', add_allergen, name='kitchen_edit_allergens')
                       )
