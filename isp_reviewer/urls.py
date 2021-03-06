from django.conf.urls import include, url
from django.contrib import admin
from isp_reviewer.views import IndexView
from isp_reviewer.settings import local

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ndt/', include('NDT.urls')),
    url(r'^stats/', include('stats.urls')),
    url(r'^isp/', include('isp.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^faq/', include('faq.urls')),
    url(r'^locations', include('locations.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': local.MEDIA_ROOT}),
    url(r'^.*$', IndexView.as_view(), name='index')
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



