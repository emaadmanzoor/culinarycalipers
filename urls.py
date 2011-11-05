from django.conf.urls.defaults import patterns, include, url
from calipers.views import index, diff
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calipers_django.views.home', name='home'),
    # url(r'^calipers_django/', include('calipers_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', index),
    (r'^diff/$', diff)
)

urlpatterns += staticfiles_urlpatterns()