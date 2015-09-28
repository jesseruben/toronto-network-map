__author__ = 'fuad'
from rest_framework import serializers
from .models import Country, City, Region

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'localized_name')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'localized_name')

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('name', 'localized_name')
