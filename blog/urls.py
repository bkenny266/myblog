from django.http import HttpResponseRedirect
from django.conf.urls import patterns, include, url
import blog.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', blog.views.blog_page),
	url(r'^(\d+)$', blog.views.blog_page),
	url(r'^create_post/$', blog.views.create_post_page),
	url(r'^edit_post/(\d+)$', blog.views.edit_post_page),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
