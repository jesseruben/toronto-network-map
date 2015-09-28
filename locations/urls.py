from locations.views import CountryViewSet, CityViewSet, RegionViewSet
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'country', CountryViewSet, base_name='country')
router.register(r'city', CountryViewSet, base_name='city')
router.register(r'region', CountryViewSet, base_name='region')

urlpatterns = [url(r'^', include(router.urls))]
