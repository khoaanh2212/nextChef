from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views

from .sitemaps import sitemaps
from recipe import urls as recipe_urls
from books import urls as book_urls
from chefs import urls as chefs_urls
from library import urls as library_urls
from embed import urls as embed_urls
from emailing import urls as emailing_urls
from subscribers import urls as subscribers_urls
from products import urls as products_urls
from search import urls as search_urls
from colls import urls as collections_urls
from kitchen import urls as kitchen_urls
from explore import urls as explore_urls
from pricing import urls as pricing_urls
from costing import urls as costing_urls
from product import urls as product_urls

# import urls_api_v1

admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^$', 'explore.views.recommended', name='home'),
    url(r'^$', 'landing.views.landing', name='home'),
    url(r'^7c622f5467f64d02bd1c29058da64b4d$', 'landing.views.bii_landing', name='bii_home'),
    url(r'^taste-of-london$', 'landing.views.taste_of_london', name='taste_of_london'),
    url(r'^product/', include(product_urls)),
    url(r'^explore/', include(explore_urls)),
    url(r'^search/', include(search_urls)),
    url(r'^recipe/', include(recipe_urls)),
    url(r'^kitchen/', include(kitchen_urls)),
    url(r'^book/', include(book_urls)),

    url(r'^chefs/', include(chefs_urls)),
    url(r'^library/', include(library_urls)),
    url(r'^products/', include(products_urls)),
    url(r'^collections/', include(collections_urls)),
    url(r'^embed/', include(embed_urls)),
    url(r'^emailing/', include(emailing_urls)),
    url(r'^subscribers/', include(subscribers_urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^pricing/', include(pricing_urls)),
    url(r'^costing/', include(costing_urls)),

    # API
    url(r'^0/', include('books.urls_api')),
    url(r'^0/', include('chefs.urls_api')),
    url(r'^0/', include('notifications.urls_api')),
    url(r'^0/', include('recipe.urls_api')),
    url(r'^0/', include('costing.urls_api')),
    url(r'^0/.*$', RedirectView.as_view()),

    url(r'^1/banners/', include('banners.urls_api_v1')),
    url(r'^1/books/', include('books.urls_api_v1')),
    url(r'^1/colls/', include('colls.urls_api_v1')),
    url(r'^1/chefs/', include('chefs.urls_api_v1')),
    url(r'^1/', include('recipe.urls_api_v1')),
    url(r'^1/', RedirectView.as_view()),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^cbt-admin/clear-cache/?$', 'backend.views.clear_cache', name='clear-cache'),
    url(r'^cbt-admin/', include(admin.site.urls)),

    url(r'^jobs/?$', TemplateView.as_view(template_name='jobs/jobs.html'), name="jobs"),
    # LEGACY URLs
    url(r'^kitchen/recipe/(?P<pk>[^/]*)$', 'recipe.views.recipe_shared', name='recipe-shared'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )

# Sitemaps URLs
urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$',
        cache_page(86400)(sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
)

# For all other urls that doesnt match we send a 410 Gone response
urlpatterns += patterns('',
                        url(r'^', 'backend.views.raise_gone', name='backend_raise_gone'),
                        )
