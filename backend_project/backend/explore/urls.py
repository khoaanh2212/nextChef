from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'explore.views.recommended', name='explore'),
                       url(r'^following/?$', 'explore.views.following', name='following'),
                       )