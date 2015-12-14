from .models import Contact
from rest_framework.response import Response
from .serializers import ContactSerializer
from rest_framework import generics, status
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get('email', None)
        subject = data.get('subject', None)
        message = data.get('message', None)
        try:
            email = EmailMessage(subject, email + ' : ' + message, to=[settings.CONTACT_EMAIL])
            email.send()
            return Response({
                'status': _('Success'),
                'message': _('Your message is successfully sent.')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e.message)
            return Response({
                'status': _('Fail'),
                'message': _('Internal server error in sending the message. Try again later')
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
