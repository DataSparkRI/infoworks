from django.conf.urls import url
from front_page import views

urlpatterns = [
    url(r'^search$', views.search, name="search_page")
    ]

