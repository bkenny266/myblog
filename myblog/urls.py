from django.conf.urls import patterns, include, url
from blog.views import log_out#, redirect_to_blog
from django.http import HttpResponseRedirect
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
#	url(r'^$', redirect_to_blog),
	url(r'^blog/', include('blog.urls')),
	url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
	url(r'^logout/$', log_out),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
