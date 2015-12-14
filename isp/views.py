from .models import ISP, Plan
from NDT.models import NDT
from .serializers import ISPSerializer, PlanSerializer
from NDT.serializers import NDTSerializerSmall
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
import logging

# getting an instance of the logger
logger = logging.getLogger(__name__)


class ISPModelViewSet(viewsets.ModelViewSet):
    queryset = ISP.objects.all()
    serializer_class = ISPSerializer
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        data = dict()
        try:
            isp = ISP.objects.get(pk=pk)
            isp_serializer = ISPSerializer(isp)
            data['isp'] = isp_serializer.data
            ndt_list = NDT.objects.filter(isp_name=isp.name)
            ndt_serializer = NDTSerializerSmall(ndt_list.order_by('-created')[:5], many=True)
            data['tests'] = ndt_serializer.data
            return Response(data)
        except ObjectDoesNotExist:
            return Response({'status': _('Bad request'), 'message': _('ISP does not exist.')},
                            status=status.HTTP_404_NOT_FOUND)


class PlanModelViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    http_method_names = ['get']
