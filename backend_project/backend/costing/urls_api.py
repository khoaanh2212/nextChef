from django.conf.urls import patterns, include, url

from . import api


urlpatterns = patterns(
    '',
    url(r'^costing-list$', api.CostingListView.as_view()),
    url(r'^custom-ingredient', api.CostingView.as_view()),
    url(r'^costing-generic-ingredient', api.CostingGenericView.as_view()),
    url(r'^generic-ingredient', api.GenericIngredientView.as_view()),
    url(r'^duplicate-ingredient', api.CostingIngredientDuplicateView.as_view()),
)
