from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^v1/recipe/(?P<slug>[^/]*)-(?P<id>[^/]*)$', 'embed.views.recipe', name='recipe-embed'),
                       )
