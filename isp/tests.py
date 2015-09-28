from django.test import TestCase
from .models import ISP, Plan
from NDT.models import NDT
import json
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import logging

# getting an instance of the logger
logger = logging.getLogger(__name__)

def approx_equal(a, b, tol):
    return abs(a - b) < tol

class ISPModelTests(TestCase):
    def setUp(self):
        self.isp1 = ISP.objects.create(name='rogers', website='rogers.ca', phone=6476078460, support_phone=1800,
                                       rating=1.5, facebook='rogers.facebook.com', twitter='rogers.twitter.com',
                                       support_link='support.rogers.com')
        self.isp1.save()
        self.isp2 = ISP.objects.create(name='bell', website='bell.ca', phone=9052342345, support_phone=2100,
                                       rating=0.5, facebook='bell.facebook.com', twitter='bell.twitter.com',
                                       support_link='support.bell.com')
        self.isp2.save()
        self.plan1 = Plan.objects.create(isp=self.isp1, price=99.99, download_rate=10, upload_rate=6,
                                         bandwidth_limit=200, limited_offer=True, link='plan1.com')
        self.plan1.save()
        self.plan2 = Plan.objects.create(isp=self.isp1, price=23.87, download_rate=3, upload_rate=1,
                                         bandwidth_limit=20, link='plan2.com')
        self.plan2.save()
        self.plan3 = Plan.objects.create(isp=self.isp2, price=199.99, download_rate=100, upload_rate=50,
                                         bandwidth=False, limited_offer=True, link='plan3.com')
        self.plan3.save()

    def tearDown(self):
        self.plan3.delete()
        self.plan2.delete()
        self.plan1.delete()
        self.isp2.delete()
        self.isp1.delete()

    def test_isp_model_create(self):
        isp = ISP.objects.get(name='rogers')
        self.assertEqual(isp.website, 'rogers.ca')
        self.assertEqual(isp.phone, 6476078460)
        self.assertEqual(isp.support_phone, 1800)
        self.assertTrue(approx_equal(1.5, isp.rating, 0.01), True)
        self.assertEqual(isp.facebook, 'rogers.facebook.com')
        self.assertEqual(isp.twitter, 'rogers.twitter.com')
        self.assertEqual(isp.support_link, 'support.rogers.com')

    def test_isp_model_update(self):
        isp = ISP.objects.get(name='bell')
        isp.website = 'bell2.ca'
        isp.save()
        new_isp = ISP.objects.get(name='bell')
        self.assertEqual(new_isp.website, 'bell2.ca')

    def test_isp_has_multiple_plans(self):
        isp1 = ISP.objects.get(name='rogers')
        plan_list = Plan.objects.filter(isp=isp1)
        self.assertEqual(plan_list.count(), 2)
        isp2 = ISP.objects.get(name='bell')
        plan_list = Plan.objects.filter(isp=isp2)
        self.assertEqual(plan_list.count(), 1)

    def test_isp_plan_foreign_key_relationship(self):
        isp1 = ISP.objects.get(name='rogers')
        plan_list = isp1.plans
        self.assertEqual(plan_list.count(), 2)
        isp2 = ISP.objects.get(name='bell')
        plan_list = isp2.plans
        self.assertEqual(plan_list.count(), 1)

class ISPViewTests(APITestCase):
    def setUp(self):
        self.isp1 = ISP.objects.create(name='rogers', website='rogers.ca', phone=6476078460, support_phone=1800,
                                       rating=1.5, facebook='rogers.facebook.com', twitter='rogers.twitter.com',
                                       support_link='support.rogers.com')
        self.isp1.save()
        self.isp2 = ISP.objects.create(name='bell', website='bell.ca', phone=9052342345, support_phone=2100,
                                       rating=0.5, facebook='bell.facebook.com', twitter='bell.twitter.com',
                                       support_link='support.bell.com')
        self.isp2.save()
        self.plan1 = Plan.objects.create(isp=self.isp1, price=99.99, download_rate=10, upload_rate=6,
                                         bandwidth_limit=200, limited_offer=True, link='plan1.com', name='plan1')
        self.plan1.save()
        self.plan2 = Plan.objects.create(isp=self.isp1, price=23.87, download_rate=3, upload_rate=1,
                                         bandwidth_limit=20, link='plan2.com', name='plan2')
        self.plan2.save()
        self.plan3 = Plan.objects.create(isp=self.isp2, price=199.99, download_rate=100, upload_rate=50,
                                         bandwidth=False, limited_offer=True, link='plan3.com', name='plan3')
        self.plan3.save()
        self.ndt = NDT.objects.create(download_rate=444, upload_rate=33, latency=30, isp_name=self.isp1.name,
                                      latitude=170.23539, longitude=120.34)
        self.ndt.save()
        self.ndt2 = NDT.objects.create(download_rate=445, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt2.save()
        self.ndt3 = NDT.objects.create(download_rate=446, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt3.save()
        self.ndt4 = NDT.objects.create(download_rate=447, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt4.save()
        self.ndt_wrong = NDT.objects.create(download_rate=997, upload_rate=33, latency=30, isp_name=self.isp1.name,
                                            latitude=170.23539, longitude=120.34)
        self.ndt_wrong.save()
        self.ndt5 = NDT.objects.create(download_rate=448, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt5.save()
        self.ndt6 = NDT.objects.create(download_rate=449, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt6.save()
        self.ndt7 = NDT.objects.create(download_rate=450, upload_rate=33, latency=30, isp_name=self.isp2.name,
                                       latitude=170.23539, longitude=120.34)
        self.ndt7.save()
        self.isp_url_list = reverse('isp-list')
        self.url_retrieve_isp1 = reverse('isp-detail', kwargs={'pk': self.isp1.id})
        self.url_retrieve_isp2 = reverse('isp-detail', kwargs={'pk': self.isp2.id})
        self.plan_url_list = reverse('plan-list')
        self.url_retrieve_plan1 = reverse('plan-detail', kwargs={'pk': self.plan1.id})
        self.url_retrieve_plan2 = reverse('plan-detail', kwargs={'pk': self.plan2.id})
        self.url_retrieve_plan3 = reverse('plan-detail', kwargs={'pk': self.plan3.id})

    def tearDown(self):
        self.plan3.delete()
        self.plan2.delete()
        self.plan1.delete()
        self.isp2.delete()
        self.isp1.delete()
        self.ndt.delete()
        self.ndt2.delete()
        self.ndt3.delete()
        self.ndt4.delete()
        self.ndt5.delete()
        self.ndt6.delete()
        self.ndt7.delete()
        self.ndt_wrong.delete()

    def test_isp_modelviewset_get_list_response(self):
        response = self.client.get(self.isp_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_isp_modelviewset_get_retrieve_response(self):
        response = self.client.get(self.url_retrieve_isp1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_isp_modelviewset_get_list_functionality(self):
        response = self.client.get(self.isp_url_list)
        expected_response = 'rogers'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)
        expected_response = 'bell'
        self.assertEqual(json.loads(response.content)[1]['name'], expected_response)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_isp_modelviewset_get_retrieve_functionality(self):
        response = self.client.get(self.url_retrieve_isp2)
        expected_response = 450
        self.assertEqual(json.loads(response.content)['tests'][0]['download_rate'], expected_response)
        expected_response = 449
        self.assertEqual(json.loads(response.content)['tests'][1]['download_rate'], expected_response)
        expected_response = 448
        self.assertEqual(json.loads(response.content)['tests'][2]['download_rate'], expected_response)
        expected_response = 447
        self.assertEqual(json.loads(response.content)['tests'][3]['download_rate'], expected_response)
        expected_response = 446
        self.assertEqual(json.loads(response.content)['tests'][4]['download_rate'], expected_response)

    def test_plan_get_list_response(self):
        response = self.client.get(self.plan_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plan_get_retrieve_response(self):
        response = self.client.get(self.url_retrieve_plan1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plan_modelviewset_get_list_functionality(self):
        response = self.client.get(self.plan_url_list)
        expected_response = 'plan1'
        self.assertEqual(json.loads(response.content)[0]['name'], expected_response)
        expected_response = 'plan2.com'
        self.assertEqual(json.loads(response.content)[1]['link'], expected_response)
        expected_response = True
        self.assertEqual(json.loads(response.content)[2]['limited_offer'], expected_response)
        expected_response = self.isp2.id
        self.assertEqual(json.loads(response.content)[2]['isp'], expected_response)
        # There should be 3 plans
        self.assertEqual(len(json.loads(response.content)), 3)

    def test_plan_modelviewset_get_retrieve_functionality(self):
        response = self.client.get(self.url_retrieve_plan3)
        expected_response = False
        self.assertEqual(json.loads(response.content)['bandwidth'], expected_response)


