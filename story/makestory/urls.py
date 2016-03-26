from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^$', views.index, name='input'),
    url(r'process/$', views.process, name='process'),
    url(r'output/$', views.output, name='output'),
    url(r'fail/$', views.fail, name='fail'),
]