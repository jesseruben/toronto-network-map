from django.test import TestCase
from .models import NDT, NDTProfile, Server, Web100
import json
from django.core.urlresolvers import reverse
from django.db import transaction
from locations.models import Country
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from isp.models import ISP
import datetime
import logging
import time

# getting an instance of the logger
logger = logging.getLogger(__name__)


def approx_equal(a, b, tol):
    return abs(a - b) < tol


class NDTModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='richard', email='r@test.com')
        self.user.save()
        self.ndt = NDT.objects.create(download_rate=444, upload_rate=33, latency=30, nominal_upload_rate=35,
                                      nominal_download_rate=500, latitude=170.23539, longitude=120.34)
        self.isp = ISP.objects.create(name='rogers', website='rogers.ca', phone=4124124141, support_phone=1800,
                                      rating=1.5, facebook='rogers.facebook.com', twitter='rogers.twitter.com',
                                      support_link='support.rogers.com')
        self.isp.save()

        self.country = Country(name=u'France')
        self.country.save()
        self.ndt_profile = NDTProfile.objects.create(user=self.user, name='name', service_type='PUBLIC',
                                                     country=self.country, isp=self.isp)
        self.ndt_profile.save()

    def tearDown(self):
        self.isp.delete()
        self.ndt.delete()
        self.ndt_profile.delete()
        self.user.delete()

    def test_check_ndt_using_id(self):
        ndt = NDT.objects.get(id=1)
        self.assertEqual(ndt.upload_rate, 33)

    def test_update_ndt(self):
        ndt = NDT.objects.get(id=1)
        ndt.latitude = 99.999
        ndt.save()
        validation_ndt = NDT.objects.get(id=1)
        self.assertEqual(approx_equal(float(validation_ndt.latitude), 99.999, 0.01), True)

    def test_check_ndt_profile_using_name(self):
        ndt_profile = NDTProfile.objects.get(name='name')
        self.assertEqual(ndt_profile.service_type, 'PUBLIC')

    def test_ndt_profile_update(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        ndt_profile.name = 'name2'
        ndt_profile.save()
        validation_ndt_profile = NDTProfile.objects.get(id=1)
        self.assertEqual(validation_ndt_profile.name, 'name2')

    def test_ndt_profile_null_values(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        self.assertEqual(ndt_profile.latitude, None)
        self.assertEqual(ndt_profile.longitude, None)
        self.assertEqual(ndt_profile.nominal_download_rate, None)
        self.assertEqual(ndt_profile.nominal_upload_rate, None)
        self.assertEqual(ndt_profile.bandwidth, None)
        self.assertEqual(ndt_profile.price, None)
        self.assertEqual(ndt_profile.contract, False)
        self.assertEqual(ndt_profile.vpn, None)
        self.assertEqual(ndt_profile.rating_general, None)
        self.assertEqual(ndt_profile.rating_customer_service, None)
        self.assertEqual(ndt_profile.country, self.country)
        self.assertEqual(ndt_profile.city, None)
        self.assertEqual(ndt_profile.promotion, None)
        self.assertNotEqual(ndt_profile.service_type, None)
        self.assertNotEqual(ndt_profile.name, None)

    def test_ndt_profile_update_null_field(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        ndt_profile.nominal_download_rate = 65.54
        ndt_profile.save()
        validation_ndt_profile = NDTProfile.objects.get(id=1)
        self.assertEqual(approx_equal(float(validation_ndt_profile.nominal_download_rate), 65.54, 0.01), True)

    def test_ndt_profile_update_null_boolean_field(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        ndt_profile.vpn = True
        ndt_profile.save()
        validation_ndt_profile = NDTProfile.objects.get(id=1)
        self.assertTrue(validation_ndt_profile.vpn)

    def test_check_if_user_and_ndt_profile_connected(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        self.assertEqual(ndt_profile.user.id, self.user.id)

    def test_ndt_profile_isp_connected(self):
        ndt_profile = NDTProfile.objects.get(id=1)
        self.assertEqual(ndt_profile.isp.name, self.isp.name)
        self.assertEqual(ndt_profile.isp.facebook, self.isp.facebook)

    def test_ndt_profile_isp_connected_get_isp(self):
        isp = ISP.objects.get(id=1)
        self.assertEqual(self.ndt_profile.isp.phone, isp.phone)

    def test_ndt_profile_isp_connected_after_update(self):
        isp = ISP.objects.get(id=1)
        isp.name = 'Rogers2'
        isp.save()
        ndt_profile = NDTProfile.objects.get(isp=self.isp)
        self.assertEqual(isp.name, ndt_profile.isp.name)


class NDTViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='name', email='name@test.com')
        self.user.set_password('password')
        self.user.save()
        self.user2 = User.objects.create(username='name2', email='name2@test.com')
        self.user2.set_password('password')
        self.user2.save()
        self.client = APIClient()
        self.client.login(email='name@test.com', password='password')
        with transaction.atomic():
            self.ndt = NDT.objects.create(download_rate=444, upload_rate=33, latency=30,
                                          latitude=170.23539, longitude=120.34)
            self.ndt2 = NDT.objects.create(download_rate=2, upload_rate=2, latency=2, rating_general=2,
                                           latitude=22.222, longitude=99.901, isp_name='django')
            self.ndt3 = NDT.objects.create(download_rate=877, upload_rate=101, latency=30, rating_general=4,
                                           latitude=110.23539, longitude=110.34, isp_name='python')
        self.isp = ISP.objects.create(name='rogers', website='rogers.ca', phone=4124124141, support_phone=1800,
                                      rating=1.5, facebook='rogers.facebook.com', twitter='rogers.twitter.com',
                                      support_link='support.rogers.com')
        self.isp.save()
        self.ndt_profile = NDTProfile.objects.create(user=self.user, name='name', service_type='PUBLIC', isp=self.isp)
        self.ndt_profile_2 = NDTProfile.objects.create(user=self.user, name='name2', service_type='PUBLIC',
                                                       isp=self.isp)
        self.ndt_profile_3 = NDTProfile.objects.create(user=self.user, name='name3', service_type='BUSINESS',
                                                       isp=self.isp)
        # the next two lines use special syntax for reversing URLs with '-'
        self.ndt_url = reverse('test-list')
        self.ndt_url_retrieve = reverse('test-detail', kwargs={'pk': self.ndt.id})
        self.ndt_profile_url = reverse('profile-list')
        self.ndt_profile_url_retrieve_1 = reverse('profile-detail', kwargs={'pk': self.ndt_profile.id})
        self.ndt_profile_url_retrieve_2 = reverse('profile-detail', kwargs={'pk': self.ndt_profile_2.id})
        self.ndt.save()
        self.ndt2.save()
        self.ndt_profile.save()
        self.ndt_profile_2.save()
        self.ndt_profile_3.save()

    def tearDown(self):
        self.isp.delete()
        self.ndt.delete()
        self.ndt2.delete()
        self.ndt_profile.delete()
        self.ndt_profile_2.delete()
        self.ndt_profile_3.delete()

    def test_ndt_modelviewset_get(self):
        response = self.client.get(self.ndt_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ndt_profile_modelviewset_get(self):
        response = self.client.get(self.ndt_profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ndt_profile_modelviewset_get_functionality(self):
        response = self.client.get(self.ndt_profile_url, format='json')
        expected_response = 'name'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)
        expected_response = 'PUBLIC'
        self.assertEqual(json.loads(response.content)[0]['service_type'], expected_response)

    def test_ndt_modelviewset_post(self):
        response = self.client.post(self.ndt_url, {'download_rate': '32', 'blob': 'hi',
                                                   'upload_rate': '21', 'latency': '29'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ndt_modelviewset_post_no_download_rate(self):
        response = self.client.post(self.ndt_url, {'upload_rate': '21.4', 'latency': '29',
                                                   }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ndt_modelviewset_post_no_upload_rate(self):
        response = self.client.post(self.ndt_url, {'download_rate': '32.2', 'latency': '29',
                                                   }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ndt_modelviewset_post_functionality(self):
        response = self.client.post(self.ndt_url, {'download_rate': '32', 'upload_rate': '21', 'latency': '29',
                                                   'blob': 'hello'},
                                    format='json')
        response = self.client.get(self.ndt_url, format='json')
        expected_response = 32
        self.assertEqual(json.loads(response.content)[3]['download_rate'], expected_response)

    def test_ndt_modelviewset_retrieve_functionality(self):
        response = self.client.get(self.ndt_url_retrieve)
        expected_response = 444
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['download_rate'], expected_response)

    def test_ndt_modelviewset_update_functionality(self):
        response = self.client.put(reverse('test-detail', kwargs={'pk': self.ndt.id}),
                                   {'download_rate': '32', 'upload_rate': '21', 'latency': '29', 'city': 'Toronto',
                                    'hash': self.ndt.hash},
                                   format='json')
        expected_response = 'Toronto'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ndt = NDT.objects.get(pk=1)
        self.assertEqual(ndt.city, expected_response)

    def test_ndt_modelviewset_search_download_gte(self):
        response = self.client.get(self.ndt_url + '?download_rate__gte=400')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = 444
        self.assertEqual(json.loads(response.content)[0]['download_rate'], expected_response)
        expected_response = 877
        self.assertEqual(json.loads(response.content)[1]['download_rate'], expected_response)

    def test_ndt_modelviewset_search_double_gte(self):
        response = self.client.get(self.ndt_url + '?download_rate__gte=400&upload_rate__gte=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = 877
        self.assertEqual(json.loads(response.content)[0]['download_rate'], expected_response)

    def test_ndt_modelviewset_search_exact(self):
        response = self.client.get(self.ndt_url + '?upload_rate=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = 2
        self.assertEqual(json.loads(response.content)[0]['download_rate'], expected_response)

    def test_ndt_modelviewset_update_old_ndt(self):
        self.ndt.created = self.ndt.created - datetime.timedelta(hours=2)
        self.ndt.save()
        response = self.client.put(reverse('test-detail', kwargs={'pk': self.ndt.id}),
                                   {'download_rate': '32', 'upload_rate': '21', 'latency': '29', 'city': 'Toronto',
                                    'hash': self.ndt.hash},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ndt_modelviewset_update_ndt_hash_wrong(self):
        response = self.client.put(reverse('test-detail', kwargs={'pk': self.ndt.id}),
                                   {'download_rate': '32', 'upload_rate': '21', 'latency': '29', 'city': 'Toronto',
                                    'hash': 'wrong_hash'},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_post(self):
        response = self.client.post(self.ndt_profile_url, {'name': 'Robert', 'service_type': 'BUSINESS',
                                                           'isp': self.isp.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ndt_profile_modelviewset_post_no_name(self):
        response = self.client.post(self.ndt_profile_url, {'service_type': 'BUSINESS'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ndt_profile_modelviewset_post_no_service_type(self):
        response = self.client.post(self.ndt_profile_url, {'name': 'Robert'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ndt_profile_modelviewset_post_functionality(self):
        response = self.client.post(self.ndt_profile_url, {'name': 'Robert', 'service_type': 'BUSINESS',
                                                           'isp': self.isp.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        profile = NDTProfile.objects.get(user=self.user, name='Robert')
        self.assertEqual(profile.service_type, 'BUSINESS')

    def test_ndt_profile_modelviewset_get_functionality_2(self):
        response = self.client.get(self.ndt_profile_url)
        expected_response = 'name'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)

    def test_ndt_profile_modelviewset_get_inactive(self):
        self.ndt_profile.active = False
        self.ndt_profile.save()
        response = self.client.get(self.ndt_profile_url)
        self.assertEqual(json.loads(response.content)[0]['name'], 'name2')

    def test_ndt_profile_modelviewset_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.ndt_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_get_retrieve(self):
        response = self.client.get(self.ndt_profile_url_retrieve_1)
        expected_response = 'name'
        self.assertEqual(json.loads(response.content)['name'], expected_response)

    def test_ndt_profile_modelviewset_get_retrieve_inactive(self):
        self.ndt_profile_2.active = False
        self.ndt_profile_2.save()
        response = self.client.get(self.ndt_profile_url_retrieve_2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_ndt_profile_modelviewset_get_retrieve_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.ndt_profile_url_retrieve_1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_post_update(self):
        profile = NDTProfile.objects.create(name='Robert', service_type='BUSINESS', isp=self.isp, user=self.user)

        response = self.client.put(reverse('profile-detail', kwargs={'pk': profile.id}),
                                   {'name': 'Robert', 'service_type': 'PUBLIC', 'isp': self.isp.id}, format='json')
        profile = NDTProfile.objects.get(user=self.user, name='Robert')
        self.assertEqual(profile.service_type, 'PUBLIC')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ndt_profile_modelviewset_post_update_not_owner(self):
        self.client.logout()
        self.client.login(email='name2@test.com', password='password')
        response = self.client.put(reverse('profile-detail', kwargs={'pk': self.ndt_profile.id}),
                                   {'name': 'Richard', 'service_type': 'PUBLIC', 'isp': self.isp.id}, format='json')
        profile = NDTProfile.objects.get(pk=1)
        self.assertEqual(profile.name, 'name')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_destroy(self):
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        response = self.client.delete(reverse('profile-detail', kwargs={'pk': self.ndt_profile.id}))
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        ndt_profile = NDTProfile.objects.get(pk=self.ndt_profile.id)
        self.assertEqual(ndt_profile.active, False)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_ndt_profile_modelviewset_destroy_not_owner(self):
        self.client.logout()
        self.client.login(email='name2@test.com', password='password')
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        response = self.client.delete(reverse('profile-detail', kwargs={'pk': self.ndt_profile.id}))
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        ndt_profile = NDTProfile.objects.get(pk=self.ndt_profile.id)
        self.assertEqual(ndt_profile.active, True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_destroy_anonymous(self):
        self.client.logout()
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        response = self.client.delete(reverse('profile-detail', kwargs={'pk': self.ndt_profile.id}))
        ndt_profile_list = NDTProfile.objects.all()
        self.assertEqual(ndt_profile_list.count(), 3)
        ndt_profile = NDTProfile.objects.get(pk=self.ndt_profile.id)
        self.assertEqual(ndt_profile.active, True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ndt_profile_modelviewset_filter_name_exact(self):
        response = self.client.get(self.ndt_profile_url+'?name=name')
        expected_response = 'name'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)
        expected_response = 'PUBLIC'
        self.assertEqual(json.loads(response.content)[0]['service_type'], expected_response)

    def test_ndt_profile_modelviewset_filter_service_type_exact(self):
        response = self.client.get(self.ndt_profile_url+'?service_type=PUBLIC')
        expected_response = 'PUBLIC'
        self.assertEqual(json.loads(response.content)[0]['service_type'], expected_response)
        self.assertEqual(json.loads(response.content)[1]['service_type'], expected_response)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_ndt_profile_modelviewset_filter_name_and_service_type(self):
        response = self.client.get(self.ndt_profile_url+'?name=name2&service_type=PUBLIC')
        expected_response = 'PUBLIC'
        self.assertEqual(json.loads(response.content)[0]['service_type'], expected_response)
        expected_response = 'name2'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_ndt_profile_modelviewset_filter_name_icontains_success(self):
        response = self.client.get(self.ndt_profile_url+'?name__icontains=na')
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_ndt_profile_modelviewset_filter_name_icontains_no_result(self):
        response = self.client.get(self.ndt_profile_url+'?name__icontains=yummy')
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_ndt_profile_modelviewset_filter_nonsense_url(self):
        response = self.client.get(self.ndt_profile_url+'?sfwfr=fssw')
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_ndt_profile_modelviewset_filter_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.ndt_profile_url+'?name=name')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ServerViewTests(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(name=u'Canada')
        self.country1.save()
        self.server1 = Server.objects.create(name='server1', url='server.canada.com', country=self.country1)
        self.server1.save()
        self.country2 = Country.objects.create(name=u'USA')
        self.country2.save()
        self.server2 = Server.objects.create(name='server2', url='server.america.com', country=self.country2)
        self.server2.save()
        self.server_url_list = self.server_url_create = reverse('server-list')

    def tearDown(self):
        self.server1.delete()
        self.server2.delete()
        self.country1.delete()
        self.country2.delete()

    def test_server_viewset_get_list(self):
        response = self.client.get(self.server_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['name'], "server1")
        self.assertEqual(json.loads(response.content)[1]['name'], "server2")


class Web100ViewTests(APITestCase):
    def setUp(self):
        self.ndt = NDT.objects.create(download_rate=23, upload_rate=5, latency=3, latitude=123.35478,
                                      longitude=140.5432, nominal_download_rate=25, nominal_upload_rate=6)
        self.ndt.save()

        self.web100 = Web100.objects.create(ndt=self.ndt, blob='{"blob_json": "hello_there"}')
        self.web100.save()
        self.web100_url_list = self.web100_url_create = reverse('web100-list')

    def tearDown(self):
        self.web100.delete()
        self.ndt.delete()

    def test_web100_viewset_get_list(self):
        response = self.client.get(self.web100_url_list)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_web100_viewset_post_create(self):
        allNDT = NDT.objects.all()
        response = self.client.post(self.web100_url_create, {'hash': '',
                                                             'blob': '{"blob_json": "create_new"}',
                                                             'upload_rate': 12, 'download_rate': 23})
        self.assertIsNotNone(response.data['hash'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        web100 = Web100.objects.get(pk=2)
        newAllNDT = NDT.objects.all()
        self.assertNotEquals(allNDT, newAllNDT)
        self.assertEqual(web100.blob, '{"blob_json": "create_new"}')

    def test_web100_viewset_multi_create(self):
        response = self.client.post(self.web100_url_create, {'hash': '',
                                                             'blob': '{"blob_json": "create_new"}',
                                                             'upload_rate': 10, 'download_rate': 23})
        self.assertIsNotNone(response.data['hash'])
        web1 = Web100.objects.get(pk=2)
        self.assertEquals(web1.ndt.id, 2)
        response = self.client.post(self.web100_url_create, {'hash': response.data['hash'],
                                                             'blob': '{"blob_json": "create_new"}',
                                                             'upload_rate': 11, 'download_rate': 24})
        self.assertIsNotNone(response.data['hash'])
        web2 = Web100.objects.get(pk=3)
        self.assertEquals(web2.ndt.id, 2)
        response = self.client.post(self.web100_url_create, {'hash': response.data['hash'],
                                                             'blob': '{"blob_json": "create_new"}',
                                                             'upload_rate': 12, 'download_rate': 25})
        self.assertIsNotNone(response.data['hash'])
        ndt_object = NDT.objects.get(hash=response.data['hash'])
        web3 = Web100.objects.get(pk=4)
        self.assertEquals(web3.ndt.id, 2)
        self.assertEquals(ndt_object.average_index, 3)
        self.assertEquals(ndt_object.upload_rate, 11)
        self.assertEquals(ndt_object.download_rate, 24)
