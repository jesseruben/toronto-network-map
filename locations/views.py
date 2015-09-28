from django.shortcuts import render
from rest_framework import status, viewsets, mixins
from .models import Country, Region, City
from .serializers import CountrySerializer, RegionSerializer, CitySerializer

# Create your views here.
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
