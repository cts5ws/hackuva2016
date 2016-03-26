from django.conf.urls import patterns, url
from makestory import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^process/$', views.process, name='process'),
    url(r'^output/$', views.output, name='output'),
    url(r'^fail/$', views.fail, name='fail'),
    url(r'^$', views.index, name='input'),
)