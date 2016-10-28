from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^unsubscribe/(?P<user_hash>[^/]*)$', 'emailing.views.unsubscribe', name='emailing_unsubscribe'),
                       )
