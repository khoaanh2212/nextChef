from django.http import HttpResponseForbidden

import elasticutils
from rest_framework import exceptions, parsers, renderers, response, status
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, CSRFCheck
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from chefs.models import Auths


class CookboothAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_CB_AUTH')
        if not token:
            return None

        try:
            token = Auths.objects.valid_token(token)
        except Auths.DoesNotExist:
            pass
            raise exceptions.AuthenticationFailed('Invalid token')

        user = token.chef

        token.update_use(request)
        token.save()

        return (user, token)

    def authenticate_header(self, request):
        return 'CB-auth'


def request_from_app(request):
    token = request.META.get('HTTP_CB_AUTH')
    if not token:
        return False
    return True


class CookboothAPIView(GenericAPIView):
    authentication_classes = (CookboothAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    paginate_by = 6
    paginate_by_param = 'limit'

    def handle_exception(self, exc):
        """
        Customize exception handling
        """
        if isinstance(exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)):
            return HttpResponseForbidden('No user credentials\n')
        elif isinstance(exc, exceptions.PermissionDenied):
            return HttpResponseForbidden(exc.detail)
        return super(CookboothAPIView, self).handle_exception(exc)

    def raise_invalid_credentials(self, msg=None):
        """
        Utility function used when some authenticated user tries to
        access a resource for whom it does not have authorization
        """
        if msg is None:
            msg = 'Invalid user credentials\n'
        raise exceptions.PermissionDenied(msg)

    def invalid_serializer_response(self, serializer):
        """
        Utility function used to create a response from an invalid serializer
        """
        errors = [{'field': f, 'message': "\n".join(errs)}
                  for f, errs in serializer.errors.iteritems()]
        for i, error in enumerate(errors):
            if error['field'] == 'non_field_errors':
                del errors[i]['field']
                break

        payload = {
            'code': 400,
            'message': 'Invalid parameters',
            'raw': errors,
        }
        return response.Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def invalid_request(self, msg):
        """
        Utility to function to create a bad request response
        """
        payload = {
            'code': 400,
            'message': msg,
        }
        return response.Response(payload, status=status.HTTP_400_BAD_REQUEST)

    def paginate_queryset(self, queryset, page_size=None):
        """
        Replace elasticutils search with django objects
        """
        # TODO: a search with pk__in with somehow maintaining order of elasticsearch
        # Now it is N queries if N objects
        ret = super(CookboothAPIView, self).paginate_queryset(queryset, page_size)
        if isinstance(ret.object_list, elasticutils.contrib.django.S):
            ret.object_list = [obj.get_object() for obj in ret.object_list]
        return ret


class CookboothWebAPIView(APIView):
    permission_classes = (AllowAny, )
    authentication_classes = (SessionAuthentication, )
    parser_classes = (parsers.FileUploadParser, parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer, )
