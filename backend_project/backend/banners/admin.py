from django.contrib import admin

from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'text')

admin.site.register(Banner, BannerAdmin)