from rest_framework import viewsets, mixins
from .models import Country, Region, City
from .serializers import CountrySerializer, RegionSerializer, CitySerializer


class CountryViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RegionViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
