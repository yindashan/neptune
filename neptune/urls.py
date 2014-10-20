from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neptune.views.home', name='home'),
    # url(r'^neptune/', include('neptune.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'common.views.index',name="index"),
    url(r'^accounts/login/', 'common.views.index',name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^file/', include('file.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^organization/', include('organization.urls')),
    url(r'^dynamicconf/', include('dynamicconf.urls')),
    url(r'^applyonline/', include('applyonline.urls')),
    url(r'^softform/', include('softform.urls')),
    url(r'^server/', include('server.urls')),
    url(r'^apppackage/', include('apppackage.urls')),
    url(r'^action/', include('action.urls')), 
    url(r'^schedule/', include('schedule.urls')),     
    url(r'^djangosalt/', include('djangosalt.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
