from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin

from .api import NavbarSearchRecipesListView, SearchRecipesListView

from recipe.models import Recipes

urlpatterns = patterns('',
                       url(r'^$', 'search.views.search', name='search'),
                       url(r'^navbar/$', NavbarSearchRecipesListView.as_view(), name='search_navbar_recipes_list'),
                       url(r'^page/$', SearchRecipesListView.as_view(), name='search_page_recipes_list'),
                       )
