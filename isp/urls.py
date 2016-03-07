from django.conf.urls import include, url
from isp.views import ISPModelViewSet, PlanModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'providers', ISPModelViewSet, base_name='isp')
router.register(r'plans', PlanModelViewSet, base_name='plan')

urlpatterns = [url(r'^', include(router.urls))]
