from django.conf.urls import url
from api_infowork import views

urlpatterns = [
    url(r'^$', views.api, name="api_infowork"),
    url(r'^clean_memcached', views.clean_memcached, name="clean_memcached"),
    url(r'^search/data', views.data, name="data"),
    url(r'^search/overtime', views.overtime, name="overtime"),
    url(r'^(?P<type>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)/(?P<detail_id>[\w-]+).js$', views.highchart_js, name="highchart_js")
    ]

