import json

from django.http import HttpResponse
from rest_framework.response import Response
from api_utils.views import CookboothAPIView


class RegistrationValidation(CookboothAPIView):
    def get_authenticators(self):
        # Deactivate all authentication for signup
        if self.request.method.lower() == 'post':
            return ()
        return super(RegistrationValidation, self).get_authenticators()

    def get_permissions(self):
        # Deactivate all authentication for login
        if self.request.method.lower() == 'post':
            return ()
        return super(RegistrationValidation, self).get_permissions()

    def post(self, request):
        from domain.chefs.chef.ChefService import ChefService
        response = {}
        event_json = json.loads(request.body)
        try:

            chefService = ChefService.new()
            chef = chefService.getByEmails(event_json['email']);
            if chef:
                response = {'valid': False}
            else:
                response = {'valid': True}
        except KeyError, e:
            response = {'valid': False}

        return Response(response)
