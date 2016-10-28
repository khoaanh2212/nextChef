from django.conf.urls import patterns, url

from . import api


urlpatterns = patterns('',
    url(r'^profile/?$', 'library.views.profile', name='profile'),
    url(r'^(?P<slug>[^/]*)-(?P<id>[^/]*)/?$', 'library.views.library', name='library'),

    url(r'^book/(?P<book_id>[^/]*)/recipes/$', api.BookRecipesListView.as_view(),
        name='library_book_recipes'),
    url(r'^(?P<chef_id>[^/]*)/restaurant/upload/image/$', api.UploadRestaurantImageView.as_view(),
        name='library_upload_restaurant_image'),
    url(r'^(?P<chef_id>[^/]*)/avatar/upload/image/$', api.UploadAvatarImageView.as_view(),
        name='library_upload_avatar_image'),
    url(r'^(?P<chef_id>[^/]*)/cover/upload/image/$', api.UploadCoverImageView.as_view(),
        name='library_upload_cover_image'),
    url(r'^(?P<chef_id>[^/]*)/recipes/?$', api.ChefRecipesListView.as_view(),
        name='library_chef_recipes'),
    url(r'^(?P<chef_id>[^/]*)/(?P<name>[^/]*)/recipes/?$', api.ChefRecipesByNameListView.as_view(),
        name='library_chef_recipes_by_name'),
    url(r'^(?P<chef_id>[^/]*)/following/?$', api.ListFollowingView.as_view(),
        name='library_chef_following'),
    url(r'^(?P<chef_id>[^/]*)/followers/?$', api.ListFollowersView.as_view(),
        name='library_chef_followers'),
)
