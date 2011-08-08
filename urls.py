from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'journal.views.home', name='home'),
    # url(r'^journal/', include('journal.foo.urls')),
    (r'^$', 'main.views.index'),
    (r'^post/$', 'main.views.post'),
    (r'^register/$', 'main.views.register'),
    (r'^login/$', 'main.views.login'),
    (r'^logout/$', 'main.views.logout'),
    (r'^profile/$', 'main.views.profile'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
