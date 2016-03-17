from django.conf.urls import url
from front_page import views

urlpatterns = [
    url(r'^search$', views.search, name="search_page"),
    url(r'^search/schools-and-districts', views.landing_page, name="landing_page"),
    url(r'^school/(?P<slug>[\w-]+)$', views.school, name="school"),
    url(r'^school/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.school_detail, name="school_detail"),
    url(r'^district/(?P<slug>[\w-]+)$', views.district, name="district"),
    url(r'^district/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.district_detail, name="district_detail"),
    url(r'^state$', views.state, name="state"),
    url(r'^state/(?P<slug>[\w-]+)$', views.states, name="states"),
    url(r'^state/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.state_detail, name="state_detail"),
    url(r'^understanding-data/dictionary$',views.dictionary,name="dictionary"),
    ]

