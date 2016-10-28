from django.conf.urls import url

from . import views

app_name = 'pricing'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(template_name='pricing/pricing.html'), name='pricing'),
    url(r'^enterprise/upgrade/', views.enterprise_upgrade, name='enterprise_upgrade')
]
