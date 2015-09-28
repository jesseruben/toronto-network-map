from django.conf.urls import include, url
from isp.views import ISPModelViewSet, PlanModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'isp', ISPModelViewSet, base_name='isp')
router.register(r'plan', PlanModelViewSet, base_name='plan')

urlpatterns = [url(r'^', include(router.urls))]
