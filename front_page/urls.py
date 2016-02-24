from django.conf.urls import url
from front_page import views

urlpatterns = [
    url(r'^search$', views.search, name="search_page"),
    url(r'^report/(?P<report_type>[\w-]+)/(?P<code>[\w-]+)$', views.report, name="report"),
    ]

