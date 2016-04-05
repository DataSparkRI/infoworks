from django.conf.urls import url
from front_page import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^search$', views.search, name="search_page"),
    url(r'^search/schools-and-districts', views.landing_page, name="landing_page"),
    url(r'^school/(?P<slug>[\w-]+)$', views.school, name="school"),
    url(r'^school/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.school_detail, name="school_detail"),
    url(r'^school/(?P<slug>[\w-]+)/history$', views.schools_history, name="schools_history"),
    url(r'^school/(?P<slug>[\w-]+)/history/(?P<school_year>[\w-]+)$', views.schools_history_detail, name="schools_history_detail"),    url(r'^district/(?P<slug>[\w-]+)$', views.district, name="district"),
    url(r'^school/(?P<slug>[\w-]+)/overtime$', views.school_overtime, name="school_overtime"),
    url(r'^district/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.district_detail, name="district_detail"),
    url(r'^district/(?P<slug>[\w-]+)/history$', views.districts_history, name="districts_history"),
    url(r'^district/(?P<slug>[\w-]+)/history/(?P<school_year>[\w-]+)$', views.districts_history_detail, name="districts_history_detail"),    url(r'^state$', views.state, name="state"),
    url(r'^district/(?P<slug>[\w-]+)/overtime$', views.district_overtime, name="district_overtime"),
    url(r'^state/(?P<slug>[\w-]+)$', views.states, name="states"),
    url(r'^state/(?P<slug>[\w-]+)/history$', views.states_history, name="states_history"),
    url(r'^state/(?P<slug>[\w-]+)/history/(?P<school_year>[\w-]+)$', views.states_history_detail, name="states_history_detail"),
    url(r'^state/(?P<slug>[\w-]+)/(?P<indicator_id>[\w-]+)/(?P<school_year>[\w-]+)/(?P<detail_slug>[\w-]+)$', views.state_detail, name="state_detail"),
    url(r'^state/(?P<slug>[\w-]+)/overtime$', views.state_overtime, name="state_overtime"),
    url(r'^understanding-data/dictionary$',views.dictionary,name="dictionary"),
    ]

