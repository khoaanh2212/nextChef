from django.conf.urls import patterns, url
from banners.api_v1 import BannersListView

urlpatterns = patterns('',
                       url(r'^list/?$', BannersListView.as_view(), name='banners-list')
)

