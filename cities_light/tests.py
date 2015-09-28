# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .forms import CountryForm, CityForm
from .models import Country, City


class FormTestCase(TestCase):
    def testCountryFormNameAndContinentAlone(self):
        form = CountryForm({'name': 'Spain', 'continent': 'EU', 'phone': '98'})
        self.assertTrue(form.is_valid(), )
        form.save()

    def testCityFormNameAndCountryAlone(self):
        country = Country(name='France')
        country.save()
        form = CityForm({'name': 'Paris', 'country': country.pk})
        self.assertTrue(form.is_valid())
        form.save()


class SaveTestCase(TestCase):
    def testCountryAsciiAndSlug(self):
        country = Country(name='áó éú')
        country.save()

        self.assertEqual(country.name_ascii, 'ao eu')
        self.assertEqual(country.slug, 'ao-eu')

    def testCityAsciiAndSlug(self):
        country = Country(name='áó éú')
        country.save()
        city = City(name='áó éú', country=country)
        city.save()

        self.assertEqual(city.name_ascii, 'ao eu')
        self.assertEqual(city.slug, 'ao-eu')
