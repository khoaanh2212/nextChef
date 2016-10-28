from django.conf.urls import patterns, include, url

from . import api


urlpatterns = patterns(
    '',
    # Recipes
    url(r'^books/(?P<book_pk>\d+)/recipes$', api.RecipeView.as_view()),
    url(r'^books/(?P<book_pk>\d+)/recipes/(?P<pk>\d+)$', api.RecipeView.as_view()),

    # Photos
    url(r'^books/(?P<book_pk>\d+)/photos$', api.PhotoView.as_view()),

    # Books
    url(r'^books$', api.BookView.as_view()),
    url(r'^books/(?P<pk>\d+)$', api.BookView.as_view()),

    url(r'^books/(?P<pk>\d+)/collaborators$', api.CollaboratorView.as_view()),
)
