from datetime import timedelta

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from api_utils.views import CookboothAPIView

from .models import Device, Notification, NotificationType, LocalNotification
from .serializers import (ApiDeviceSerializer, ApiDevicePaginatedSerializer,
                          ApiNotificationSerializer, ApiNotificationPaginatedSerializer,
                          ApiLocalNotificationSerializer)


class DeviceView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiDeviceSerializer
    pagination_serializer_class = ApiDevicePaginatedSerializer

    def post(self, request, *args, **kwargs):
        """
        Create device
        """
        if 'pk' in kwargs:
            raise Http404()

        # Danger: this is implemented because it was this way in the original API. But, the way
        # it is, any user can access another user device (if he knows the identificator)
        try:
            device = Device.objects.get(identificator=request.POST.get('identificator', None))
            serializer = ApiDeviceSerializer(device)
            return Response({'device': serializer.data})
        except Device.DoesNotExist:
            pass

        serializer = ApiDeviceSerializer(data=request.DATA)
        serializer.user = request.user
        if serializer.is_valid():
            device = serializer.save()
            return Response({'device': serializer.data})
        return self.invalid_serializer_response(serializer)

    def delete(self, request, *args, **kwargs):
        """
        Delete device
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Device, pk=kwargs['pk'])

        if obj.chef != request.user:
            self.raise_invalid_credentials()

        obj.delete()
        return Response({'response': {'return': True}})

    def get(self, request, *args, **kwargs):
        """
        View devices
        """
        if 'pk' in kwargs:
            raise Http404()

        self.queryset = request.user.devices.all()
        return self.list(request, *args, **kwargs)


class NotificationView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiNotificationSerializer
    pagination_serializer_class = ApiNotificationPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        View notifications
        """
        if 'pk' in kwargs:
            raise Http404()

        if 'action' in kwargs:
            if kwargs['action'] == 'unread':
                return Response({'response': {'return': request.user.notifications.unread().count()}})
            else:
                raise Http404()

        request.user.notifications.unread().update(unread=False)
        self.queryset = request.user.notifications.filter(creation_date__lte=now()).order_by('-creation_date').all()
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update notification
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Notification, pk=kwargs['pk'])

        if obj.chef != request.user:
            self.raise_invalid_credentials()

        serializer = ApiNotificationSerializer(obj, data=request.DATA, partial=True)
        if serializer.is_valid():
            notification = serializer.save()
            return Response({'response': {'return': True}})
        return self.invalid_serializer_response(serializer)

    def delete(self, request, *args, **kwargs):
        """
        Delete notification
        """
        if 'pk' not in kwargs:
            raise Http404()

        obj = get_object_or_404(Notification, pk=kwargs['pk'])

        if obj.chef != request.user:
            self.raise_invalid_credentials()

        obj.delete()
        return Response({'response': {'return': True}})


class NotificationTestView(ListModelMixin, CookboothAPIView):
    def get(self, request, *args, **kwargs):
        """
        Test
        """
        return Response({'response': {'return': True}})


class LocalNotificationsListView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiLocalNotificationSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the messages for local notifications to a chef
        """
        user_lang = kwargs.get('language', 'en')
        if user_lang not in ('en', 'es', 'ca', 'de', 'fr', 'pt'):
            user_lang = 'en'

        yesterday = now() - timedelta(days=1)

        if request.user.creation_date >= yesterday:
            query = LocalNotification.objects.messages_for_new_users(request.user, user_lang)
        else:
            query = LocalNotification.objects.messages_for_old_users(request.user, user_lang)

        self.queryset = query
        return self.list(request, *args, **kwargs)
