from django.utils import translation
from django.conf import settings

class AdminLocaleURLMiddleware:

    def process_request(self, request):
        if request.path.startswith('/admin'):
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        else:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
