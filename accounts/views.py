from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from accounts.models import User, UserUID
from accounts.serializers import UserSerializer, UserUIDSerializer, PasswordSerializer
from accounts.permissions import IsOwner
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import transaction
from django.core.urlresolvers import reverse
import logging
import hashlib
from random import SystemRandom
import datetime
import json
import os
import string
import codecs
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    # This is the user viewset. It is used for creating/validating a user given information.
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'generic'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # override default value of id to lookup in username framework
    lookup_field = 'username'

    errs = {
        'ser_invalid': _("UserViewSet.create failed because serializer was invalid"
                         " because of these errors : {0}"),
        'exception': _("UserViewSet.create failed because an exception happened. Exception: {0}")
    }

    msgs = {
        'finish_success': _("UserViewSet.create is finished successfully. User: {0}"),
        'account_created': _("Your account is created")
    }

    def get_permissions(self):
        logger.info("UserViewSet.get_permissions is called.")
        # check for permission of update and destroy
        # If the HTTP method of the request ('GET', 'POST', etc) is "safe", then anyone can use that endpoint.
        # permissions are loaded either from permission.py or rest framework
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        # @TODO fix this permission classes
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsOwner(),)

    def create(self, request):
        data = request.data
        try:
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                email = serializer.validated_data['email']
                user = User.objects.create_user(**serializer.validated_data)
                # originally response would return serializer.data
                logger.info(self.msgs['finish_success'].format(user.log_guid))
                return Response({
                    'status': _('Success'),
                    'message':self.msgs['account_created']
                }, status=status.HTTP_201_CREATED)
            logger.error(self.errs['ser_invalid'].format(serializer.errors))
            return Response({
                # Translators: This message is generated during user creation
                'status': _('Bad request'),
                'message': _('User info is invalid.'),
                'errors': 'Validation error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(self.errs['exception'].format(e.message))
            return Response({
                'status': _('Bad request'),
                'message': e.message
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    """
    We won't use viewset because we don't need create and update here
    While APIView does not handle everything for us, it does give us much more than standard Django views do.
    In particular, views.APIView are made specifically to handle AJAX requests.
    """
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'generic'

    errs = {
        'user_inactivated': _("LoginView.post failed because the user account is not activated. User: {0}"),
        'no_account': _("LoginView.post failed because no account was found with the given email address. Email: {0}")
        }

    msgs = {
        'login_success': _("User has successfully logged in. User: {0}"),
        'login_msg': _('You are logged in successfully.'),
        'cannot_login': _('You can not log in with this account.'),
        'combination_invalid': _('Username/password combination invalid.')
    }

    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)
        if account is not None:
            # TODO : Add more type of the accounts along with it's response to the frontend
            if account.is_active:
                login(request, account)
                serialized = UserSerializer(account)
                logger.info(self.msgs['login_success'].format(request.user.log_guid))
                return Response({
                    'account': serialized.data,
                    'status': _('Success'),
                    'message': self.msgs['login_msg']
                }, status=status.HTTP_200_OK)
            else:
                logger.info(self.errs['user_inactivated'].format(request.user.log_guid))
                # Right now we remove the accounts from the DB upon deactivation, so we should never get into this state
                return Response({
                    'status': _('Unauthorized'),
                    'message': self.msgs['cannot_login']
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.info('User attempts to login with credentials and do not exist')
            return Response({
                'status': _('Unauthorized'),
                'message': self.msgs['combination_invalid']
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    def post(self, request):
        if request.user.is_authenticated():
            logger.info("LogoutView.post is called. User: {0}".format(request.user.log_guid))
        else:
            logger.info("LogoutView.post is called by anonymous user.")
        logout(request)
        return Response({
            'status': _('Success'),
            'message': _('You are successfully logged out.')
        }, status=status.HTTP_200_OK)


class UpdatePasswordView(views.APIView):
    """
    @input: password, new_password, confirm_password
    @description: changes the password of logged in user
    """

    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'generic'
    queryset = User.objects.all()
    serializer_class = PasswordSerializer

    errs = {
        'ser_not_valid': _("UpdatePasswordView.post failed because user serializer not valid. Data: {0}"),
        'exception': _("UpdatePasswordView.post failed because exception occurred. Exception: {0}"),
        'user_inactive': _("UpdatePasswordView.post failed because user account is not active. User: {0}"),
        'user_not_found': _("UpdatePasswordView.post failed because user account is not found. User: {0}"),
        'server_error': _("Internal server error happened when trying to update password."),
        'combination_invalid': _("Username/password combination invalid."),
        'password_mismatch': _("New Password and Confirm Password do not match."),
        }

    msgs = {
        'finish_success': _("UpdatePasswordView.post finished successfully. User: {0}"),
        'update_pass_success': _("Successfully updated the user password."),
        'cannot_update_pass': _('You cannot update the password on this account.'),
    }

    def post(self, request):
        logger.info("UpdatePasswordView.post is called. User: {0}".format(request.user.log_guid))
        # TODO: check if front end sends a json file or normal request
        data = request.data
        update_password_serializer = self.serializer_class(data=data)
        if update_password_serializer.is_valid():
            password = update_password_serializer.validated_data['password']
            account = authenticate(email=request.user.email, password=password)
            if account is not None:
                if account.is_active:
                    new_password = update_password_serializer.validated_data['new_password']
                    try:
                        # we use partial to avoid passing required fields into serializer
                        serializer = UserSerializer(account, data={'password': new_password}, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            account = authenticate(email=request.user.email, password=new_password)
                            login(request, account)
                            logger.info(self.msgs['finish_success'].format(request.user.log_guid))
                            return Response({
                                'status': _('Success'), 'message': self.msgs['update_pass_success']},
                                status=status.HTTP_200_OK)
                        else:
                            logger.error(self.errs['ser_not_valid'].format(data))
                            return Response({'status': _('Bad request'), 'message': serializer.errors},
                                            status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        logger.exception(self.errs['exception'].format(e.message))
                        return Response({'status': _('Bad request'), 'message': self.errs['server_error']},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    logger.error(self.errs['user_inactive'].format(request.user.log_guid))
                    return Response({'status': _('Unauthorized'), 'message': self.msgs['cannot_update_pass']},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                logger.error(self.errs['combination_invalid'])
                return Response({
                    'status': _('Unauthorized'), 'message': self.errs['combination_invalid']},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.error(update_password_serializer.errors)
            return Response({'status': 'Bad request', 'message': self.errs['password_mismatch'],
                             'errors': 'Validation error'},
                            status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(views.APIView):
    """
    Sets a UUID for the user model and send forgot password link
    Does not set the new password for the user
    """
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'generic'

    errs = {
        'ser_not_valid': _("ForgotPasswordView.post failed because user serializer not valid. Data: {0}"),
        'exception': _("ForgotPasswordView.post failed because exception occurred. User: {0}, Exception: {1}"),
        'user_not_found': _("ForgotPasswordView.post failed because user account is not found. User: {0}"),
        'server_error': _("Internal server error in sending forgot password email"),
        'smtp_fail': _("ForgotPasswordView.post failed because SMTP mail server failed or an error happened while "
                       "trying to send the email, error: {0}"),
        'UID_invalid': _("ForgotPasswordView.post failed because UserUID serializer was not valid."
                         " User: {0}, GUID: {1}, date: {2}")
        }

    msgs = {
        'finish_success': _("ForgotPasswordView.post finished successfully. User: {0}"),
        'success': _("If registered, an email will be sent to: {0}"),
        'update_pass_success': _("Successfully updated the user password."),
        'cannot_update_pass': _('You cannot update the password on this account.'),
    }

    def post(self, request):
        data = json.loads(request.body)
        receiver_email = data.get('email', None)
        try:
            account = User.objects.get(email=receiver_email)
        except ObjectDoesNotExist:
            logger.exception(self.errs['user_not_found'].format(receiver_email))
            return Response({
                'status': _('Success'),
                'message': self.msgs['success'].format(receiver_email)
            }, status=status.HTTP_200_OK)
        if account is not None and receiver_email:
            data['guid'] = hashlib.sha512(str(SystemRandom().getrandbits(512))).hexdigest()
            data['user'] = account.id
            date = datetime.datetime.utcnow()
            data['expiration_date'] = date + datetime.timedelta(days=settings.FORGOT_PASSWORD_GUID_EXPIRATION)
            try:
                serializer = UserUIDSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    try:
                        language_cookie_value = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
                        file_path = os.path.join(settings.EMAIL_TEMPLATE_FA_LOCATION)

                        if language_cookie_value == "en":
                            file_path = os.path.join(settings.EMAIL_TEMPLATE_EN_LOCATION)
                        file_handler = codecs.open(file_path, encoding="utf-8")
                        email_content = file_handler.read()
                        str_with_username = string.replace(email_content, '[username]', account.username)
                        absolute_url = request.build_absolute_uri(reverse('setpassword') + data['guid'])
                        personalized_email = string.replace(str_with_username, '[link]', absolute_url)
                        email = EmailMessage('Forgot Password Email', personalized_email, to=[receiver_email])
                        email.send()
                        logger.info(self.msgs['finish_success'].format(account.log_guid))
                        return Response({
                            'status': _('Success'),
                            'message': self.msgs['success'].format(receiver_email)
                        }, status=status.HTTP_200_OK)
                    except Exception, e:
                        logger.exception(self.errs['smtp_fail'].format(e.message))
                        return Response({
                            'status': _('Fail'),
                            'message': self.errs['server_error']
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    logger.error(self.errs['UID_invalid'].format(account.log_guid, data['guid'], date))
                    return Response({
                        'status': _('Bad request'),
                        'message': self.errs['server_error']
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.exception(self.errs['exception'].format(account.log_guid, e.message))
                return Response({
                    'status': _('Bad request'),
                    'message': self.errs['server_error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(self.errs['user_not_found'].format(account.log_guid))
            return Response({
                'status': _('Bad request'),
                'message': self.errs['user_not_found'].format(receiver_email)
            }, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordView(views.APIView):
    """
    Set the new password for the user who has forgotten his password and has received the activation link
    """

    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'generic'

    errs = {
        'ser_not_valid': _("SetPasswordView.post failed because UID serializer was invalid. "
                           "GUID: {0}, user_id: {1}, new_expiration_Date: {2}"),
        'exception': _("SetPasswordView.post failed because an exception happened. GUID: {0}, exception: {1}"),
        'server_error': _("Internal server error in setting password. Try again later"),
        'GUID_invalid': _("SetPasswordView.post failed because no user_uid was found with the given GUID. GUID: {0}"),
        'GUID_expired': _("SetPasswordView.post failed because the GUID is expired. "
                          "GUID: {0}, expiration_date: {1}, current_time: {2}"),
        'GUID_none': _("SetPasswordView.post failed because account was none. GUID: {0}")
        }

    msgs = {
        'activation_invalid': _('The activation link is not valid'),
        'password_mismatch': _('New Pass and Confirm Password do not match.'),
        'finish_success': _("SetPasswordView.post finished successfully. GUID: {0}"),
        'success': _("If registered, an email will be sent to: {0}"),
        'update_pass_success': _("Successfully updated the user password."),
        'cannot_update_pass': _('You cannot update the password on this account.'),
    }

    def post(self, request):
        data = json.loads(request.body)
        guid = data.get('guid', None)
        logger.info("SetPasswordView.post is called. GUID: {0}".format(guid))

        password_serializer = PasswordSerializer(data=data, partial=True)
        if not password_serializer.is_valid():
            return Response({
                'status': _('Bad request'),
                'message': self.msgs['password_mismatch'],
                'errors': 'Validation error'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_uid = UserUID.objects.get(guid=guid)
        except ObjectDoesNotExist:
            logger.exception(self.errs['GUID_invalid'].format(guid))
            return Response({
                'status': _('Bad request'),
                'message': self.msgs['activation_invalid']
            }, status=status.HTTP_400_BAD_REQUEST)

        now_offset_aware = timezone.make_aware(datetime.datetime.utcnow(), timezone.get_current_timezone())

        if user_uid.expiration_date < now_offset_aware:
            logger.error(self.errs['GUID_expired'].format(guid, user_uid.expiration_date, now_offset_aware))
            return Response({
                'status': _('Bad request'),
                'message': self.msgs['activation_invalid']
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = User.objects.get(id=user_uid.user_id)
        except ObjectDoesNotExist:
            logger.exception(self.errs['GUID_invalid'].format(guid))
            return Response({
                'status': _('Fail'),
                'message': self.errs['server_error']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if account is not None:
            se_data = dict()
            se_data['password'] = password_serializer.validated_data['new_password']
            se_data['confirm_password'] = password_serializer.validated_data['confirm_password']
            se_data['email'] = account.email
            se_data['username'] = account.username
            se_data['log_guid'] = account.log_guid
            try:
                with transaction.atomic():
                    serializer = UserSerializer(account, data=se_data)
                    if serializer.is_valid():
                        serializer.save()
                        # We need to mark the forgotpassword GUID as expired
                        uid_data = dict()
                        uid_data['guid'] = guid
                        uid_data['user'] = user_uid.user_id
                        uid_data['expiration_date'] = datetime.datetime.utcnow()
                        uidSerializer = UserUIDSerializer(user_uid, data=uid_data)

                        if uidSerializer.is_valid():
                            uidSerializer.save()
                            logger.info(self.msgs['finish_success'].format(guid))
                            return Response({
                                'status': _('Success'),
                                'message': self.msgs['update_pass_success']
                            }, status=status.HTTP_200_OK)
                        else:
                            logger.error(self.errs['ser_not_valid'].format(guid, user_uid.user_id, uid_data['expiration_date']))
                            return Response({
                                'status': _('Fail'),
                                'message': self.errs['server_error']
                            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        logger.error(self.errs['server_error'])
                        return Response({
                            'status': _('Fail'),
                            'message': self.errs['server_error']
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.exception(self.errs['exception'].format(guid, e.message))
                return Response({
                    'status': _('Bad request'),
                    'message': self.errs['server_error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.exception(self.errs['GUID_none'].format(guid))
            return Response({
                'status': _('Bad request'),
                'message': self.msgs['activation_invalid']
            }, status=status.HTTP_400_BAD_REQUEST)


class DeactivateView(views.APIView):

    errs = {
        'pass_not_valid': _("Password not valid"),
        'deactivation_fail': _("account for deactivation failed. User: {0}"),
        'unauthorized': _("User is not authorized to perform this action.")
        }

    msgs = {
        'deactivate_success': _("User account is successfully deactivated. User: {0} "),
        'delete_success': _('Successfully deleted the account.')
    }

    def post(self, request):
        if request.user.is_authenticated():
            logger.info("DeactivateView.post is called. User: {0} ".format(request.user.log_guid))
            data = json.loads(request.body)
            password = data.get('password', None)
            account = authenticate(email=request.user.email, password=password)
            if account is not None:
                account.delete()
                logger.info(self.msgs['deactivate_success'].format(request.user.log_guid))
                return Response({
                    'status': _('Success'),
                    'message': self.msgs['delete_success']
                }, status=status.HTTP_200_OK)
            logger.error(self.errs['deactivation_fail'].format(request.user.log_guid))
            return Response({
                'status': _('Bad request'),
                'message': self.errs['pass_not_valid']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info("DeactivateView.post is called on unauthenticated user")
            return Response({
                'status': _('Unauthorized'),
                'message': self.errs['unauthorized']
            }, status=status.HTTP_401_UNAUTHORIZED)
