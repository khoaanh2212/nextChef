from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<token>[^/]*)/?$', 'subscribers.views.recipes', name='subscribers_recipes'),
                       url(r'^chefs/(?P<token>[^/]*)/?$', 'subscribers.views.chefs', name='subscribers_chefs'),
                       )
