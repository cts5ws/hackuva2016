from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import makestory.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$/', include('makestory.urls')),
)
