from django.conf.urls import patterns, include, url

from . import api_v1


urlpatterns = patterns(
    '',

    # Books
    url(r'^(?P<pk>\d+)$', api_v1.BookView.as_view()),
    url(r'^(?P<pk>\d+)/buy$', api_v1.BookBuyView.as_view()),
    url(r'^for-sale$', api_v1.BooksForSaleView.as_view()),
)
