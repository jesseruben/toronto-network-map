from django.test import TestCase
from .models import Contact
import json
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class ContactModelTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(email='sth@sth.com', subject='hello', message='some message')
        self.contact.save()

    def tearDown(self):
        self.contact.delete()


    def test_contact_model_create(self):
        contact = Contact.objects.get(email='sth@sth.com')
        self.assertEqual(contact.email, 'sth@sth.com')
        self.assertEqual(contact.subject, 'hello')
        self.assertEqual(contact.message, 'some message')

class ContactViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('contact')
        self.contact = Contact.objects.create(email='sth@sth.com', subject='hello', message='some message')
        self.contact.save()

    def tearDown(self):
        self.contact.delete()

    def test_contact_view_create_response(self):
        response = self.client.post(self.url, {'email': 'test@tester.com', 'subject': 'subject',
                                               'message': 'some message'}, format='json')
        expected_response = u'Your message is successfully sent.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)


