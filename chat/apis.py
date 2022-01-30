from rest_framework import status, response, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *
from .helpers import enable_socket_notification_to_user


class UpdateNotificationIsReadValue(generics.GenericAPIView):
    '''This API is for updating the is_read peroperty of the notifications of the given user'''
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.data['user'])
        queryset = Notification.objects.filter(to_user=user, status__exact='active')
        queryset.update(is_read=True)
        enable_socket_notification_to_user(user, queryset, False, False)
        return response.Response(status=status.HTTP_200_OK)
