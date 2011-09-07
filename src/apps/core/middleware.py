from django.utils import translation
from django.conf import settings

class LocaleMiddleware(object):
    def process_request(self, request):
        translation.activate(settings.LANGUAGE_CODE)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        
        translation.deactivate()
        
        return response
