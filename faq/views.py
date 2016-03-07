from rest_framework import viewsets
from .models import Faq
from .serializers import FaqSerializer


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
