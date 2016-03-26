from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', RedirectView.as_view(pattern_name="makestory")),
    url(r'^makestory/', include('makestory.urls')),
    url(r'^admin/', include(admin.site.urls)),
)