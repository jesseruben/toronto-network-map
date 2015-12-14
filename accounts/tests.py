from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient
from .models import User, UserUID
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from django.db import transaction
from datetime import timedelta
import json
import logging

logger = logging.getLogger(__name__)


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User(email='mustache@gaga.com', username='harper')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_user_query_by_username(self):
        validation_user = User.objects.get(username='harper')
        self.assertEquals(self.user.username, validation_user.username)
        self.assertEquals(self.user.email, validation_user.email)

    def test_user_query_by_email(self):
        validation_user = User.objects.get(email='mustache@gaga.com')
        self.assertEquals(self.user.username, validation_user.username)
        self.assertEquals(self.user.email, validation_user.email)

    def test_user_update(self):
        Email = 'justin@bieber.com'
        user_temp = User.objects.get(username='harper')
        user_temp.email = Email
        user_temp.save()

        validation_user = User.objects.get(email='justin@bieber.com')
        self.assertEqual(validation_user.email, Email)


class LoginViewTests(APITestCase):
    def setUp(self):
        """
        By default, requests created with APIRequestFactory will not have CSRF validation
        applied when passed to a REST framework
        """
        cache.clear()
        self.user = User(email='rim@rim.com', username='bunny')
        self.user.set_password('gypsy_king')
        self.user.save()
        self.url = reverse('login')
        self.correct_data = {'email': 'rim@rim.com', 'password': 'gypsy_king'}
        self.wrong_data = {'email': 'peach@wherami.com', 'password': 'kiss_my_back'}

    def tearDown(self):
        self.user.delete()
        cache.clear()

    def test_login_get(self):
        response = self.client.get(self.url, self.correct_data, format='json')
        expected_response = {u'detail': u'Method "GET" not allowed.'}
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_login_wrong_credential(self):
        response = self.client.post(self.url, self.wrong_data, format='json')
        expected_response = {u'message': u'Username/password combination invalid.', u'status': u'Unauthorized'}
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_login_correct_credential(self):
        response = self.client.post(self.url, self.correct_data, format='json')
        # response dict is too long so we just check the message
        expected_response = u'You are logged in successfully.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_login_throttle_post_wrong_data(self):
        for x in range(0, 20):
            response = self.client.post(self.url, self.wrong_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url, self.wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_throttle_post_correct_data(self):
        for x in range(0, 20):
            response = self.client.post(self.url, self.correct_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.client.logout()
        response = self.client.post(self.url, self.correct_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_throttle_get(self):
        for x in range(0, 20):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class UpdatePasswordViewTests(APITestCase):
    def setUp(self):
        """
        By default, requests created with APIRequestFactory will not have CSRF validation
        applied when passed to a REST framework
        """
        self.user = User(email='name1@test.com', username='name1')
        self.user.set_password('Password12')
        self.user.save()
        self.url = reverse('updatepassword')
        self.client = APIClient()
        self.client.login(email='name1@test.com', password='Password12')
        cache.clear()

    def tearDown(self):
        self.user.delete()
        cache.clear()

    def test_update_get(self):
        response = self.client.get(self.url, {'email': 'name1@test.com', 'password': 'password'}, format='json')
        expected_response = {u'detail': u'Method "GET" not allowed.'}
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_update_post(self):
        response = self.client.post(self.url, {'password': 'Password12', 'new_password': 'New_8_chars',
                                               'confirm_password': 'New_8_chars'}, format='json')
        expected_response = u'Successfully updated the user password.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_update_post_password_mismatch(self):
        response = self.client.post(self.url, {'password': 'password', 'new_password': '1abfCdfegg',
                                               'confirm_password': '1abfCdfeggs'}, format='json')
        expected_response = u'Validation error'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['errors'], expected_response)

    def test_update_post_invalid_user(self):
        response = self.client.post(self.url, {'password': 'invalid', 'new_password': '1abfCdfegg',
                                               'confirm_password': '1abfCdfegg'}, format='json')
        expected_response = u'Username/password combination invalid.'
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_update_post_missing_arguments(self):
        response = self.client.post(self.url, {'password': 'password', 'new_password': 'newpass'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_password_regex_fail(self):
        response = self.client.post(self.url, {'password': 'Password12', 'new_password': 'newpass',
                                               'confirm_password': 'newpass'}, format='json')
        expected_response = u'Validation error'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['errors'], expected_response)

    def test_update_throttle_post(self):
        for x in range(0, 20):
            response = self.client.post(self.url, {'password': 'New_8_chars', 'new_password': 'New_8_chars',
                                                   'confirm_password': 'New_8_chars'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(self.url, {'password': 'New_8_chars', 'new_password': 'New_8_chars',
                                               'confirm_password': 'New_8_chars'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_update_throttle_get(self):
        for x in range(0, 20):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class ForgotPasswordViewTests(APITestCase):
    def setUp(self):
        """
        By default, requests created with APIRequestFactory will not have CSRF validation
        applied when passed to a REST framework
        """
        self.user = User(email='name1@test.com', username='name1')
        self.user.set_password('password')
        self.user.save()
        self.url = reverse('forgotpassword')
        self.client = APIClient()

    def tearDown(self):
        self.user.delete()

    def test_forgot_password(self):
        response = self.client.post(self.url, {'email': 'name1@test.com'}, format='json')
        expected_response = u'If registered, an email will be sent to: name1@test.com'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)
        u = UserUID.objects.get(user=self.user.id)
        self.assertEqual(u.type, 'forgotPassword')


class SetPasswordViewTests(APITestCase):
    def setUp(self):
        self.user = User(email='name1@test.com', username='name1')
        self.user.set_password('HelloJohn9')
        self.user.save()
        self.user_uid = UserUID.objects.create(guid='ZMKIO', user=self.user)
        self.user_uid.expiration_date = self.user_uid.expiration_date + timedelta(days=1)
        self.user_uid.save()
        self.user_uid_2 = UserUID.objects.create(guid='ZMKIO2', user=self.user)
        self.user_uid_2.expiration_date = self.user_uid_2.expiration_date - timedelta(days=1)
        self.user_uid_2.save()
        self.url = reverse('setpassword')
        self.client = APIClient()
        cache.clear()

    def tearDown(self):
        self.user_uid.delete()
        self.user_uid_2.delete()
        self.user.delete()
        cache.clear()

    def test_set_password_mismatch(self):
        response = self.client.post(self.url, {'new_password': 'hello', 'confirm_password': 'not_hello'}, format='json')
        expected_response = u'New Pass and Confirm Password do not match.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_set_guid_valid(self):
        response = self.client.post(self.url, {'new_password': '1Hellojack', 'confirm_password': '1Hellojack', 'guid': 'ZMKIO'},
                                    format='json')
        expected_response = u'Successfully updated the user password.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_set_guid_expired(self):
        response = self.client.post(self.url, {'new_password': 'H3elloooo', 'confirm_password': 'H3elloooo', 'guid': 'ZMKIO2'},
                                    format='json')
        expected_response = u'The activation link is not valid'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_set_guid_invalid(self):
        response = self.client.post(self.url, {'new_password': 'H3elloooo', 'confirm_password': 'H3elloooo', 'guid': 'invalid'},
                                    format='json')
        expected_response = u'The activation link is not valid'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_set_guid_missing_argument(self):
        response = self.client.post(self.url, {'confirm_password': 'hello', 'guid': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = u'Validation error'
        self.assertEqual(json.loads(response.content)['errors'], expected_response)

    def test_set_regex_fail(self):
        response = self.client.post(self.url, {'new_password': 'hello', 'confirm_password': 'hello', 'guid': 'invalid'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = u'Validation error'
        self.assertEqual(json.loads(response.content)['errors'], expected_response)

    def test_set_throttle_post(self):
        for x in range(0, 20):
            response = self.client.post(self.url, {'new_password': '1Hellojack', 'confirm_password': '1Hellojack',
                                                   'guid': 'invalid'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(self.url, {'new_password': '1Hellojack', 'confirm_password': '1Hellojack',
                                               'guid': 'invalid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_set_throttle_get(self):
        for x in range(0, 20):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class DeactivateViewTests(APITestCase):
    def setUp(self):
        self.user = User(email='name1@test.com', username='name1')
        self.user.set_password('password')
        self.user.save()
        self.url = reverse('deactivate')
        self.client = APIClient()
        self.client.login(email='name1@test.com', password='password')
        self.client2 = APIClient()

    def tearDown(self):
        self.user.delete()

    def test_deactivate_success(self):
        response = self.client.post(self.url, {'password': 'password'}, format='json')
        expected_response = u'Successfully deleted the account.'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_deactivate_fail_password_wrong(self):
        response = self.client.post(self.url, {'password': 'wrongpassword'}, format='json')
        expected_response = u'Password not valid'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_deactivate_unauthenticated_user(self):
        self.client.logout()
        response = self.client2.post(self.url, {'password': 'irrelevant'}, format='json')
        expected_response = u'User is not authorized to perform this action.'
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.content)['message'], expected_response)


class UserViewTests(APITestCase):
    """
    These test are checking registration API
    """
    def setUp(self):
        self.user = User(email='rim@rim.com', username='bunny')
        self.user.set_password('Gypsy_king2')
        self.user.save()
        self.url = reverse('register')
        self.correct_data = {'email': 'new@rim.com', 'username': 'new_user', 'password': 'Mig_mig23',
                             'confirm_password': 'Mig_mig23'}
        self.duplicate_data = {'email': 'rim@rim.com', 'username': 'sth', 'password': 'Hello1234',
                               'confirm_password': 'Hello1234'}
        self.short_pass_data = {'email': 'second@rim.com', 'username': 'grandma', 'password': 'Short',
                                'confirm_password': 'short'}
        cache.clear()

    def tearDown(self):
        self.user.delete()
        cache.clear()

    def test_register_get(self):
        response = self.client.get(self.url, self.correct_data, format='json')
        expected_response = {u'detail': u'Method "GET" not allowed.'}
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_correct_data(self):
        response = self.client.post(self.url, self.correct_data, format='json')
        expected_response = {u'status': u'Success', u'message': u'Your account is created'}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_register_duplicate_data(self):
        """
        each test is wrapped in a transaction,
        so if an exception occurs, it breaks the transaction until you explicitly roll it back.
        that's why you can't check for unique transaction without using transaction.atomic()
        :return:
        """
        with transaction.atomic():
            response = self.client.post(self.url, self.duplicate_data, format='json')
            expected_response = u'User info is invalid.'
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_register_missing_data(self):
        response = self.client.post(self.url, format='json')
        expected_response = u'User info is invalid.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)

    def test_register_short_password(self):
        response = self.client.post(self.url, self.short_pass_data, format='json')
        expected_response = u'User info is invalid.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['message'], expected_response)
        expected_response = u'Validation error'
        self.assertEqual(json.loads(response.content)['errors'], expected_response)

    def test_register_throttle_get(self):
        for x in range(0, 20):
            response = self.client.get(self.url, self.correct_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.get(self.url, self.correct_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_register_throttle_post(self):
        with transaction.atomic():
            for x in range(0, 20):
                response = self.client.post(self.url, self.duplicate_data, format='json')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            response = self.client.post(self.url, self.duplicate_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User(email='name@test.com', username='name')
        self.user.set_password('password')
        self.user.save()
        self.url = reverse('logout')
        self.client = APIClient()
        self.client.login(email='name@test.com', password='password')
        self.client2 = APIClient()

    def tearDown(self):
        self.user.delete()

    def test_logged_in(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = u'You are successfully logged out.'
        self.assertEqual(json.loads(response.content)['message'], expected_response)

