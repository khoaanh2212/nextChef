from django.conf.urls import patterns, include, url

from . import api


urlpatterns = patterns(
    '',
    url(r'^chefs/login$', api.LoginView.as_view()),

    url(r'^chefs/resetpassword$', api.ResetPasswordView.as_view()),

    url(r'^chefs/(?P<pk>\d+)/follows$', api.ChefFollowView.as_view()),
    url(r'^chefs/(?P<pk>\d+)/(?P<action>(following|followers))$', api.ChefFollowersView.as_view()),

    url(r'^chefs$', api.ChefView.as_view()),
    url(r'^chefs/(?P<pk>\d+)$', api.ChefDetailView.as_view()),

    url(r'^chefs/(?P<pk>\d+)/books$', api.ChefBooksView.as_view()),
    url(r'^chefs/(?P<pk>\d+)/drafts$', api.ChefDraftsView.as_view()),
    url(r'^chefs/(?P<pk>\d+)/photos$', api.ChefPhotosView.as_view()),
    url(r'^chefs/(?P<pk>\d+)/recipes$', api.ChefRecipesView.as_view()),

    url(r'^(?P<action>suggested)/chefs$', api.ChefSearchView.as_view()),
    url(r'^(?P<action>search)/chefs$', api.ChefSearchView.as_view()),

    url(r'^facebook$', api.FacebookView.as_view()),
    url(r'^facebook/(?P<action>friends)$', api.FacebookView.as_view()),

    url('^chefs/stripe$', api.PaymentWebhookView.as_view()),

    url('^chefs/plan$', api.PlanView.as_view(), name='get_plan'),
)
