from django.conf.urls import patterns, url

from .api import AddBookView, DeleteBookView, EditBookView, AddRecipeToBookView

urlpatterns = patterns('',
                       url(r'^checkout/(?P<id>[^/]*)/?$', 'books.views.checkout', name='book_checkout'),
                       url(r'^checkout/change/password/(?P<id>[^/]*)/?$', 'books.views.checkout_change_password', name='book_checkout_change_password'),
                       url(r'^add/?$', AddBookView.as_view(), name='books_add_book'),
                       url(r'^edit/(?P<book_id>[^/]*)/$', EditBookView.as_view(), name='books_edit_book'),
                       url(r'^delete/(?P<book_id>[^/]*)/$', DeleteBookView.as_view(), name='books_delete_book'),
                       url(r'^add/recipe/(?P<book_id>[^/]*)/(?P<recipe_id>[^/]*)/$', AddRecipeToBookView.as_view(), name='books_add_recipe_book'),
                       url(r'^(?P<id>[^/]*)/?$', 'books.views.book', name='book'),
                       )
