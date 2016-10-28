from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<slug>[^/]*)$', 'colls.views.collection', name='collection'),
                       )
