from django.conf.urls import patterns, url

from . import api_v1 as api


urlpatterns = patterns(
    '',
    url(r'^list/followings/?$', api.ChefFollowingsListView.as_view(), name='chef-followings-list'),
    url(r'^list/loves/?$', api.ChefLovesListView.as_view(), name='chef-loves-list'),
    url(r'^list/chefs/?$', api.ChefsListView.as_view(), kwargs=dict(type='all'), name='chefs-list'),
    url(r'^list/chefs/pro/?$', api.ChefsListView.as_view(), kwargs=dict(type='pro'), name='chefs-pro-list'),
    url(r'^list/chefs/foodie/?$', api.ChefsListView.as_view(), kwargs=dict(type='foodie'), name='chefs-foodie-list'),

    url(r'^by-type$', api.ChefsByTypeListView.as_view()),
    url(r'^onboard$', api.ChefsOnboardView.as_view()),

    url(r'^(?P<pk>\d+)/books$', api.ChefBooksView.as_view()),
    url(r'^(?P<pk>\d+)/recipes$', api.ChefRecipesView.as_view()),
)
