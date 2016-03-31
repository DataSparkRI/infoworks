from django.conf.urls import url
from api_infowork import views

urlpatterns = [
    url(r'^$', views.api, name="api_infowork"),
    url(r'^search/data', views.data, name="data"),
    url(r'^search/overtime', views.overtime, name="overtime"),
    ]

