from django.conf.urls import url
from front_page import views

urlpatterns = [
    url(r'^$', views.index, name="index_page")
    ]

