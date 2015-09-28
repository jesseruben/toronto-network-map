from django.conf.urls import include, url
from django.contrib import admin
from isp_reviewer.views import IndexView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ndt/', include('NDT.urls')),
    url(r'^isp/', include('isp.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^contact/', include('contact.urls')),
    url(r'^locations', include('locations.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^.*$', IndexView.as_view(), name='index')
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



