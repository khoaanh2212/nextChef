from django.conf.urls import patterns, include, url

from . import api


urlpatterns = patterns(
    '',
    # Messages for local notifications
    url(r'^notifications/local/(?P<language>.+)$', api.LocalNotificationsListView.as_view()),

    # Devices
    url(r'^notifications/devices$', api.DeviceView.as_view()),
    url(r'^notifications/devices/(?P<pk>\d+)$', api.DeviceView.as_view()),

    # Notifications
    url(r'^notifications$', api.NotificationView.as_view()),
    url(r'^notifications/(?P<action>unread)$', api.NotificationView.as_view()),
    url(r'^notifications/(?P<pk>\d+)$', api.NotificationView.as_view()),

    # Test
    url(r'^notifications/push/test$', api.NotificationTestView.as_view()),
)
