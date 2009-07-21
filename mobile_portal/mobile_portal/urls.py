from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mobile_portal/', include('mobile_portal.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^$', 'mobile_portal.core.views.index', {}, 'core_index'),
    (r'^core/ajax/update_location/$', 'mobile_portal.core.views.ajax_update_location', {}, 'core_ajax_update_location'),
    (r'^core/update_location/$', 'mobile_portal.core.views.update_location', {}, 'core_update_location'),


    (r'^crisis/$', 'mobile_portal.core.views.crisis', {}, 'core_crisis'),
    (r'^contact/', include('mobile_portal.contact.urls')),
    (r'^maps/', include('mobile_portal.maps.urls')),
    (r'^podcasts/', include('mobile_portal.podcasts.urls')),
    (r'^results/', include('mobile_portal.results.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
