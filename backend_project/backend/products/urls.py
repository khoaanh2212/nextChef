from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^related/recipes/(?P<barcode>[^/]*)/$', 'products.views.related_recipes_embed', name='products_related_recipes'),
                       )
