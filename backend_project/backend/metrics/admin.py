from django.contrib import admin

from .models import Metric


class MetricAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = ('kpi', 'created', 'segment', 'value_num', 'value_str')
    list_filter = ('kpi', 'segment',)
    search_fields = ('kpi',)
    ordering = ('-created', 'kpi')
    filter_horizontal = ()


admin.site.register(Metric, MetricAdmin)
