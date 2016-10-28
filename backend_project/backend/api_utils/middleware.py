class ApiDomainMiddleware:
    def process_request(self, request):
        request.domain = request.META.get('HTTP_HOST', '')
        if request.domain.startswith('api.'):
            request.urlconf = 'backend.urls_api'

