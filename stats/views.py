from NDT.models import NDT
from rest_framework import views
from .serializers import NDTRegionalSmall
from rest_framework.response import Response
from ipware.ip import get_ip
from geoip import geolite2
from django.db import connection
from django.db.models import Avg
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
import logging

# getting an instance of the logger
logger = logging.getLogger(__name__)


def get_location(request):
    ip = get_ip(request)
    latitude = None
    longitude = None
    if ip is not None:
        '''
           TODO: For testing purposes this is set to a static IP but it must be change to ip instead
        '''
        g = geolite2.lookup('107.161.4.218')
        latitude, longitude = g.location
    return latitude, longitude


# Returns the average of upload/download speed over time around a specified geographical area
class RegionalCircleView(views.APIView):
    def get(self, request):
        data = request.GET
        dist = data.get('dist', None)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        if latitude and longitude:
            point = [float(latitude), float(longitude)]
        else:
            point = list(get_location(request))
        ref_location = Point(point)
        truncate_date = connection.ops.date_trunc_sql('month', 'created')
        queryset = NDT.objects.extra({'created': truncate_date})
        queryset = queryset.filter(location__distance_lte=(ref_location, D(m=dist)))
        queryset = queryset.values('id', 'created', 'price', 'location', 'isp').annotate(upload=Avg('upload_rate'), download=Avg('download_rate')).order_by('created')
        serializer = NDTRegionalSmall(queryset, many=True)
        return Response(serializer.data)


# Returns the average of upload/download speed over time around a specified geographical area
class RegionalRectView(views.APIView):
    def get(self, request):
        data = request.GET
        xmin = data.get('xmin', None)
        ymin = data.get('ymin', None)
        xmax = data.get('xmax', None)
        ymax = data.get('ymax', None)
        if xmin and ymin and xmax and ymax:
            rectangle = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            queryset = NDT.objects.all()
            queryset = queryset.filter(location__within=rectangle)
            queryset = queryset.values('id', 'price', 'location', 'isp_name', 'isp', 'upload_rate', 'download_rate')
            serializer = NDTRegionalSmall(queryset, many=True)
            return Response(serializer.data)


class AllTestsView(views.APIView):
    def get(self, request):
        all_tests = len(NDT.objects.all())
        return Response(all_tests)
