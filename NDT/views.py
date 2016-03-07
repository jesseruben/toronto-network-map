from .models import NDT, NDTProfile, Server, Web100
from .serializers import NDTSerializer, NDTProfileSerializer, NDTProfileSerializerSmall
from .serializers import ServerSerializer, Web100Serializer, NDTSerializerSmall
from .permissions import IsOwnerOrReadOnly
from .filters import NDTProfileFilter, NDTFilter
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from ipware.ip import get_ip
from django.utils import timezone
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.db import transaction
import random
import urllib2
import json
import datetime
import logging

# getting an instance of the logger
logger = logging.getLogger(__name__)


def get_location(request):
    ip = get_ip(request)
    latitude = None
    longitude = None
    if ip is not None:
        try:
            if ip == "127.0.0.1":
                # call from dev
                response = urllib2.urlopen('https://freegeoip.net/json/{0}'.format('173.178.155.74')) #"random ip"
            else:
                response = urllib2.urlopen('https://freegeoip.net/json/{0}'.format(ip))
            data = json.load(response)
            latitude = data['latitude']
            longitude = data['longitude']
        except urllib2.HTTPError:
            logger.warning('freegoip.net is not reachable from the server')
    return latitude, longitude


def obfuscate_location(latitude, longitude):
    # We randomly change the latitude and longitude of the request by (-0.005, +0.005)
    if latitude is not None and longitude is not None:
        latitude_offset = float(random.randrange(-5000, 5000))/1000000
        longitude_offset = float(random.randrange(-5000, 5000))/1000000
        return float(latitude)+latitude_offset, float(longitude)+longitude_offset


class NDTModelViewSet(viewsets.ModelViewSet):
    queryset = NDT.objects.all()
    serializer_class = NDTSerializer

    def list(self, request):
        data = request.GET
        dist = data.get('dist', None)
        if dist:
            url_point = data.get('point', None)
            if url_point:
                point_array = url_point.split(",")
                point = [float(x) for x in point_array]
            else:
                point = list(get_location(request))
            ref_location = Point(point)
            queryset = NDT.objects.filter(location__distance_lte=(ref_location, D(m=dist)))
        else:
            queryset = NDT.objects.all()
        queryset = NDTFilter(request.GET, queryset=queryset)
        serializer = NDTSerializerSmall(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            ndt = NDT.objects.get(pk=pk)
            serializer = NDTSerializer(ndt)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'status': _('Bad request'), 'message': _('NDT does not exist.')},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        logger.debug('Attempting to update NDT {0}...'.format(pk))
        data = request.data
        hash = data.get('hash', None)
        try:
            ndt = NDT.objects.get(pk=pk)

            if ndt.hash != hash:
                return Response({'status': _('Unsuccessful'), 'message': _('Wrong ndt hash value')},
                                status=status.HTTP_401_UNAUTHORIZED)

            if ndt.created < timezone.now() - datetime.timedelta(hours=1):
                return Response({'status': _('Unsuccessful'), 'message': _('Cannot edit ndt more than 1 hour old.')},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = NDTSerializer(ndt, data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({'status': _('Success'), 'message': _('NDT {0} is successfully updated.'.format(pk))},
                                status=status.HTTP_200_OK)
            else:
                logger.debug('NDTSerializer is invalid. These are the errors: {0}'.format(serializer._errors))
                return Response({'status': _('Bad request'), 'message':
                                _('NDT Profile could not be updated with the received data.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        logger.debug('Attempting to create new NDT...')
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        ndt = serializer.save()
                        download_rate = serializer.validated_data['download_rate']
                        upload_rate = serializer.validated_data['upload_rate']
                        latency = serializer.validated_data['latency']
                        logger.debug('New NDT created successfully. Download Rate: {0}, '
                                     'Upload Rate: {1}, Latency: {2}'.format(download_rate, upload_rate, latency))
                        data['ndt'] = ndt.id
                        web_100_serializer = Web100Serializer(data=data)
                        if web_100_serializer.is_valid():
                            web_100_serializer.save()
                        else:
                            # raising exception so that transaction will roll back if web100serializer is invalid
                            raise ValidationError('Something went wrong when trying to create ndt.')
                except Exception as e:
                    logger.error('Exception thrown: {0}'.format(e))
                    return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'status': _('Success'), 'message': _('NDT is created.')},
                                status=status.HTTP_201_CREATED)
            logger.debug('Serializer is invalid. These are the errors: {0}'.format(serializer._errors))
            return Response({'status': _('Bad request'), 'message':
                            _('NDT could not be created with the received data.')}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)


# Available functions - list, create, retrieve, update, destroy
class NDTProfileModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = NDTProfileSerializer
    queryset = NDTProfile.objects.all()

    def list(self, request):
        if request.user.is_authenticated():
            queryset = self.queryset.filter(user=request.user, active=True)
            queryset = NDTProfileFilter(request.GET, queryset=queryset)
            serializer = NDTProfileSerializerSmall(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'status': _('Bad request'), 'message': _('You must log in first.')},
                            status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated():
            try:
                profile = NDTProfile.objects.get(pk=pk, active=True)
                serializer = NDTProfileSerializer(profile)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response({'status': _('Bad request'), 'message': _('Profile does not exist.')},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': _('Bad request'), 'message': _('You must log in first.')},
                            status=status.HTTP_401_UNAUTHORIZED)

    # with hash value, create either tries to create or update profile, and update NDT
    def create(self, request):
        logger.debug('Attempting to create new NDT Profile...')
        data = request.data
        hash = data.get('hash', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        ndt_profile = None #instantiating the profile
        existing_ndt = None #instantiating NDT
        if latitude and longitude:
            location = Point(latitude, longitude)
            data['location'] = location
        try:
            if hash:
                ndt_profile = NDTProfile.objects.get(hash=hash)
        except ObjectDoesNotExist:
            logger.debug('Frontend send a hash which is not linked to a hash {0}'.format(hash))
        try:
            if hash:
                existing_ndt = NDT.objects.get(hash=hash)
        except ObjectDoesNotExist:
            logger.warning('Frontend send a hash function to profile which was not found in NDT: {}'.format(hash))
        try:
            if ndt_profile:
                # trying to update the previous profile
                serializer = NDTProfileSerializer(ndt_profile, data=data)
            else:
                # no previous profile
                serializer = NDTProfileSerializer(data=data)
            if serializer.is_valid():
                if request.user.is_authenticated():
                    profile = serializer.save(user=request.user)
                else:
                    profile = serializer.save()
                # updating NDT model if hash value was passed by the frontend report module
                if existing_ndt:
                    existing_ndt.ndt_profile = profile
                    existing_ndt.nominal_upload_rate = profile.nominal_upload_rate
                    existing_ndt.nominal_download_rate = profile.nominal_download_rate
                    existing_ndt.price = profile.price
                    existing_ndt.city = profile.city
                    existing_ndt.province = profile.province
                    existing_ndt.bandwidth = profile.bandwidth
                    existing_ndt.service_type = profile.service_type
                    existing_ndt.rating_general = profile.rating_general
                    existing_ndt.isp_name = profile.isp_name
                    existing_ndt.isp = profile.isp
                    existing_ndt.save()
                return Response({'status': _('Success'), 'message': _('NDT Profile is created.')},
                                status=status.HTTP_201_CREATED)
            else:
                logger.debug('NDTProfileSerializer is invalid. These are the errors: {0}'.format(serializer._errors))
                return Response({'status': _('Bad request'), 'message':
                                _('NDT Profile could not be created with the received data.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.debug('Updating NDT Profile')
        data = request.data
        try:
            ndt_profile = NDTProfile.objects.get(pk=pk)

            try:
                # to check that this object belongs to the user from permissions.py
                self.check_object_permissions(request, ndt_profile)
            except APIException as e:
                logger.error('APIException thrown: {0}'.format(e))
                return Response({'status': _('Bad request'),
                                 'message': _('You do not have permissions to modify this profile')},
                                status=status.HTTP_401_UNAUTHORIZED)

            serializer = NDTProfileSerializer(ndt_profile, data=data)
            if serializer.is_valid():
                if request.user.is_authenticated():
                    serializer.save(user=request.user)
                else:
                    serializer.save()
                return Response({'status': _('Success'), 'message': _('NDT Profile is successfully updated.')},
                                status=status.HTTP_200_OK)
            else:
                logger.debug('NDTProfileSerializer is invalid. These are the errors: {0}'.format(serializer._errors))
                return Response({'status': _('Bad request'), 'message':
                                _('NDT Profile could not be updated with the received data.')},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        logger.debug('Attempting to delete NDTProfile #{0}'.format(pk))
        try:
            ndt_profile = NDTProfile.objects.get(pk=pk)
            try:
                # to check that this object belongs to the user from permissions.py
                self.check_object_permissions(request, ndt_profile)
            except APIException as e:
                logger.error('User does not have permission to edit profile object. APIException thrown: {0}'.format(e))
                return Response({'status': _('Bad request'),
                                 'message': _('You do not have permissions to modify this profile')},
                                status=status.HTTP_401_UNAUTHORIZED)
            ndt_profile.active = False
            ndt_profile.save()
            return Response({'status': _('Success'), 'message': _('NDT Profile is successfully deleted.')},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)


class ServerViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Server.objects.filter(active=True)
    serializer_class = ServerSerializer


class Web100ViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    queryset = Web100.objects.all()
    serializer_class = Web100Serializer

    def create(self, request):
        logger.debug('Attempting to create new Web100...')
        data = request.data
        blob = data.get('blob', None)
        hash = data.get('hash', None)
        download_rate = data.get('download_rate', None)
        upload_rate = data.get('upload_rate', None)
        latency = data.get('latency', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        if latitude is None or longitude is None:
            latitude, longitude = get_location(request)
        if latitude is not None and longitude is not None:
            latitude, longitude = obfuscate_location(latitude, longitude)
        else:
            logger.warning("Geoip services was not accessible.")
        try:
            if hash:
                # If existing_ndt doesn't exist, an exception is thrown which is caught by the try-catch block
                existing_ndt = NDT.objects.get(hash=hash)
                web_100_serializer = Web100Serializer(data={'blob': blob, 'ndt': existing_ndt.id})
                with transaction.atomic():
                    if web_100_serializer.is_valid():
                        web_100_serializer.save()
                        updated_ndt = NDTSerializerSmall(existing_ndt, data={'upload_rate': upload_rate,
                                                                             'download_rate': download_rate,
                                                                             'latency': latency})
                        if updated_ndt.is_valid():
                            updated_ndt.save()
                            return Response({'status': _('Success'), 'hash': hash})
                        else:
                            logger.error('There were some validation errors when updating the ndt object: '
                                         '{0}'.format(updated_ndt.errors))
                            return Response({'status': _('Bad request'), 'message':
                                            'There were some validation errors when updating the ndt object'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        logger.error('There were some validation errors when saving the Web100 object: '
                                     '{0}'.format(web_100_serializer.errors))
                        return Response({'status': _('Bad request'), 'message':
                                        'There were some validation errors when saving the Web100 object'},
                                        status=status.HTTP_400_BAD_REQUEST)

            else:
                ndt_serializer = NDTSerializerSmall(data={'download_rate': download_rate, 'upload_rate': upload_rate,
                                                          'latency': latency, 'location': Point(latitude, longitude)})
                if ndt_serializer.is_valid():
                    try:
                        with transaction.atomic():
                            ndt_object = ndt_serializer.save()
                            web_100_serializer = Web100Serializer(data={'blob': blob, 'ndt': ndt_object.id})
                            if web_100_serializer.is_valid():
                                web_100_serializer.save()
                                return Response({'status': _('Success'), 'hash': ndt_object.hash},
                                                status=status.HTTP_200_OK)
                            else:
                                logger.error('There were some validation errors when saving the Web100 object:'
                                             ' {0}'.format(web_100_serializer.errors))
                                return Response({'status': _('Bad request'), 'message': 'There were some validation'
                                                                                        ' errors when saving the Web100'
                                                                                        ' object'},
                                                status=status.HTTP_400_BAD_REQUEST)

                    except Exception as e:
                        logger.error('Exception thrown: {0}'.format(e))
                        return Response({'status': _('Bad request'), 'message': e.message},
                                        status=status.HTTP_400_BAD_REQUEST)

                else:
                    logger.error('There were some validation errors when saving the NDT '
                                 'object: {0}'.format(ndt_serializer.errors))
                    return Response({'status': _('Bad request'), 'message': 'There were '
                                                                            'some validation errors when'
                                                                            ' saving the NDT object'},
                                    status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error('Exception thrown: {0}'.format(e))
            return Response({'status': _('Bad request'), 'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
