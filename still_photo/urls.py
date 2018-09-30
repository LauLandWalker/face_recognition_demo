from django.conf.urls import url
from still_photo import views

urlpatterns = [
    url(r'^$', views.homepage, name="home"),
]