# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .models import Country, City, Region
from rest_framework import status
from django.core.urlresolvers import reverse

class SaveTestCase(TestCase):
    def testCountryAsciiAndSlug(self):
        country = Country(name='áó éú')
        country.save()

        self.assertEqual(country.name_ascii, 'ao eu')
        self.assertEqual(country.slug, 'ao-eu')

"""
class ListTests(TestCase):
    def setUp(self):

        country = Country(name='rd')
        country.save()
        city = City(name='sd', country=country)
        city.save()

        country_1 = Country(name='Canada', localized_name='CAN')
        country_1.save()
        country_1 = Country.objects.get(pk=1)

        self.country_2 = Country(name='America', localized_name='USA')
        self.city_1 = City(name='Toronto', localized_name='TOR', country=country_1)
        self.country_2.save()
        self.city_1.save()
        self.country_url = reverse('country-list')
        self.city_url = reverse('city-list')
        self.region_url = reverse('region-list')

    def tearDown(self):
        self.country_1.delete()
        self.country_2.delete()

    def test_country_list(self):
        response = self.client.get(self.country_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_list(self):
        response = self.client.get(self.city_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_region_list(self):
        response = self.client.get(self.region_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
"""