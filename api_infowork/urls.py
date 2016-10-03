from django.conf.urls import url
from api_infowork import views

urlpatterns = [
    url(r'^$', views.api, name="api_infowork"),
    url(r'^school_indicator$',views.school_indicator, name="api_school_indicator"),
    url(r'^school_tabledata$',views.school_tabledata, name="api_school_tabledata"),
    url(r'^school$',views.school, name="api_school"),
    url(r'^district$',views.district, name="api_district"),
    url(r'^district_indicator$',views.district_indicator, name="api_district_indicator"),
    url(r'^state$',views.state, name="api_state"),
    url(r'^state_indicator$',views.state_indicator, name="api_state_indicator"),
    url(r'^clean_memcached', views.clean_memcached, name="clean_memcached"),
    url(r'^search/data', views.data, name="data"),
    url(r'^search/overtime', views.overtime, name="overtime"),
    url(r'^(?P<type>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)/(?P<detail_id>[\w-]+).js$', views.highchart_js, name="highchart_js")
    ]

