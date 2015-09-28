from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import NDTProfileModelViewSet, ServerViewSet, Web100ViewSet, NDTModelViewSet

router = DefaultRouter()

router.register(r'profile', NDTProfileModelViewSet, base_name='profile')
router.register(r'server', ServerViewSet, base_name='server')
router.register(r'web100', Web100ViewSet, base_name='web100')
router.register(r'test', NDTModelViewSet, base_name='test')

urlpatterns = [url(r'^', include(router.urls))]