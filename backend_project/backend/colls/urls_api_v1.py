from django.conf.urls import patterns, url
from colls.api_v1 import CollsListView

urlpatterns = patterns('',
                       url(r'^list/?$', CollsListView.as_view(), name='colls-list'),
                       )

