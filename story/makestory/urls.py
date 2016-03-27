from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='input'),
    url(r'^output/', views.output, name='output'),
    url(r'^fail/', views.fail, name='fail'),
]