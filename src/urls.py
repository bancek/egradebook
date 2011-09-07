from django.conf.urls.defaults import *

from django.contrib import admin
from django.contrib import databrowse
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),

    url(r'^admin/docs/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^browser/(.*)', databrowse.site.root),
    
    url(r'^dijak', include('dijak.views')),
    url(r'^stars', include('stars.views')),
    url(r'^profesor', include('profesor.views')),
    
    url(r'^prijava$', 'auth.views.login_view', name='login'),
    url(r'^odjava$', 'auth.views.logout_view', name='logout'),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
