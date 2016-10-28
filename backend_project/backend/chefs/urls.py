from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from .api import ChefsListView
from .api import ChefsProsListView
from .api import ChefsFoodiesListView
from .api import FollowView
from .api import PaymentWebhookView

urlpatterns = patterns('',
                       url(r'^$', 'chefs.views.chefs_all', name='chefs'),
                       url(r'^activation/$', 'chefs.views.activation', name='activation'),
                       url(r'^pro/$', 'chefs.views.chefs_pro', name='chefs_pro'),
                       url(r'^foodies/$', 'chefs.views.chefs_foodies', name='chefs_foodies'),
                       url(r'^json/?$', ChefsListView.as_view(), name='chefs-json'),
                       url(r'^json/pros/?$', ChefsProsListView.as_view(), name='chefs-pros-json'),
                       url(r'^json/foodies/?$', ChefsFoodiesListView.as_view(), name='chefs-foodies-json'),
                       url(r'^follow/?$', FollowView.as_view(), name='chefs_follow'),
                       url(r'^delete/(?P<id>[^/]*)$', 'chefs.views.delete_chef', name='delete-chef'),
                       url(r'^payment$', 'chefs.views.select_payment', name='select-payment'),
                       url(r'^submit-payment$', 'chefs.views.submit_payment', name='submit-payment'),
                       url(r'^get-by-name-limit$', 'chefs.views.get_chef_by_name_limit',name='get_chef_by_name_limit'),
                       url(r'^get-chef-by-list-id$','chefs.views.get_chef_by_list_id',name='get_chef_by_list_id')
                       )
