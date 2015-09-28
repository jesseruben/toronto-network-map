"""
Couple djangorestframework and cities_light.

It defines a urlpatterns variables, with the following urls:

- cities-light-api-city-list
- cities-light-api-city-detail
- cities-light-api-region-list
- cities-light-api-region-detail
- cities-light-api-country-list
- cities-light-api-country-detail

If rest_framework (v2) is installed, all you have to do is add this url
include::

    url(r'^cities_light/api/', include('cities_light.contrib.restframework2')),

And that's all !
"""
from rest_framework import viewsets, relations
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework import routers

try:
    from django.conf.urls.defaults import patterns, url, include
except ImportError:
    from django.conf.urls import patterns, url, include

from ..loading import get_cities_models

Country, Region, City = get_cities_models()


class CitySerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for City.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cities-light-api-city-detail')
    country = relations.HyperlinkedRelatedField(
        view_name='cities-light-api-country-detail')
    region = relations.HyperlinkedRelatedField(
        view_name='cities-light-api-region-detail')

    class Meta:
        model = City


class RegionSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for Region.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cities-light-api-region-detail')
    country = relations.HyperlinkedRelatedField(
        view_name='cities-light-api-country-detail')

    class Meta:
        model = Region


class CountrySerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for Country.
    """
    url = relations.HyperlinkedIdentityField(
        view_name='cities-light-api-country-detail')

    class Meta:
        model = Country


class CitiesLightListModelViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against name_ascii.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(name_ascii__icontains=self.request.GET['q'])

        return queryset


class CountryModelViewSet(CitiesLightListModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class RegionModelViewSet(CitiesLightListModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class CityModelViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against search_names.
        """
        queryset = super(CitiesLightListModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            return queryset.filter(
                search_names__icontains=self.request.GET['q'])

        return queryset


router = routers.SimpleRouter()
router.register(r'cities', CityModelViewSet, base_name='cities-light-api-city')
router.register(r'countries', CountryModelViewSet,
                base_name='cities-light-api-country')
router.register(r'regions', RegionModelViewSet,
                base_name='cities-light-api-region')


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
