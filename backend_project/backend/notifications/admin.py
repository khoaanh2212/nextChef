from django.contrib import admin

from .models import LocalNotification, Notification, Device


class LocalNotificationAdmin(admin.ModelAdmin):
    list_display = ('days', 'language', 'message_type', 'message')
    search_fields = ('language', 'shop_url', 'shop_title')
    list_filter = ('days', 'language', 'message_type')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'creation_date', 'unread', 'chef', 'creator', 'followed', 'recipe', 'comment')
    search_fields = ('creator__email', 'chef__email')
    list_filter = ('creation_date', 'type',)
    readonly_fields = ('chef', 'creator', 'recipe', 'type', 'comment', 'followed')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('type', 'creation_date', 'chef', 'identificator', 'language', 'environment')
    search_fields = ('identificator', 'chef__email')
    list_filter = ('creation_date', 'type', 'environment')
    readonly_fields = ('chef', )

admin.site.register(LocalNotification, LocalNotificationAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Device, DeviceAdmin)