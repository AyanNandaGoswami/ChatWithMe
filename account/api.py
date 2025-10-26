import time
from rest_framework.generics import *
from rest_framework import status, permissions, views
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .serializers import *
from .models import FriendList
from chat.models import Notification
from chat.utils import create_new_notification
from chat.helpers import get_friend_list_with_last_message
from utils.constants.base import AUTH_TOKEN


class LoginCallbackAPI(views.APIView):
    """
    API to handle the login-callback request
    """

    def get(self, request):
        # retrieve the access token from the params and set to COOKIES
        token = request.GET.get('token')
        response = redirect('/options')

        if token:
            # set to session
            request.session['authToken'] = {
                'value': token,
                'timestamp': time.time()
            }

            response.set_cookie(
                key=AUTH_TOKEN,
                value=token,
                max_age=600,
                httponly=False,
                secure=False,
                samesite='Lax',
                path='/'
            )
        return response


class AcceptAndRejectFriendRequestAPI(GenericAPIView):
    '''
    This API is for accepting and rejecting the friend request
    it accepts a post request with notification_id, user(who will accept the request) and action(like accept/reject)
    '''
    serializer_class = AcceptRejectSerializer
    queryset = FriendList.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification_obj = serializer.validated_data['notification_obj']
        action = serializer.validated_data['action']
        if action == 'accepted':
            friend_list_obj, created = FriendList.objects.get_or_create(user=notification_obj.created_by)
            friend_list_obj.friends.add(notification_obj.to_user)

            another_list_obj, created = FriendList.objects.get_or_create(user=notification_obj.to_user)
            another_list_obj.friends.add(notification_obj.created_by)

            notification_obj.status = 'inactive'
            notification_obj.save()

            data = {
                'notification_body': f'<a href="">{notification_obj.to_user.first_name} {notification_obj.to_user.last_name}</a> accepted your friend request.',
                'created_by': notification_obj.to_user.id,
                'to_user': notification_obj.created_by.id,
                'notification_type': 'accept_or_reject'
            }
            if create_new_notification(data):
                pass
            else:
                print('notification dose not created.')

            return Response({'ack': True}, status=status.HTTP_201_CREATED)
        elif action == 'rejected':
            notification_obj.status = 'inactive'
            notification_obj.save()
            data = {
                'notification_body': f'<a href="">{notification_obj.to_user.first_name} {notification_obj.to_user.last_name}</a> rejected your friend request.',
                'created_by': notification_obj.to_user.id,
                'to_user': notification_obj.created_by.id,
                'notification_type': 'accept_or_reject'
            }
            if create_new_notification(data):
                pass
            else:
                print('notification dose not created.')
            return Response({'ack': True}, status=status.HTTP_201_CREATED)


class UnfriendAPI(GenericAPIView):
    serializer_class = UnfriendSerializer
    queryset = FriendList.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        friend_obj = get_object_or_404(FriendList, user=serializer.validated_data['user'])
        if friend_obj.friends.filter(pk=serializer.validated_data['friend'].id):
            friend_obj.friends.remove(serializer.validated_data['friend'])

        friend_obj = get_object_or_404(FriendList, user=serializer.validated_data['friend'])
        if friend_obj.friends.filter(pk=serializer.validated_data['user'].id):
            friend_obj.friends.remove(serializer.validated_data['user'])

        data = {
                'notification_body': f'<a href="">{serializer.validated_data["user"].first_name} {serializer.validated_data["friend"].last_name}</a> break friendship with you.',
                'created_by': serializer.validated_data['user'].id,
                'to_user': serializer.validated_data['friend'].id,
                'notification_type': 'accept_or_reject'
            }
        if create_new_notification(data):
            pass
        else:
            print('notification dose not created.')

        return Response(get_friend_list_with_last_message(serializer.validated_data['user'].id), status=status.HTTP_200_OK)


class SendFriendRequest(GenericAPIView):
    '''
    This API is for sending the friend request
    and after sending a frienquest it will create a notification for that user
    '''
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['user'])
        friend = get_object_or_404(User, username=request.data['friend'])
        print(user, friend)
        notification_obj = Notification.objects.filter(Q(created_by=user) & Q(to_user=friend) & Q(status__exact="active") & Q(notification_type__exact="send")).last()
        # print(notification_obj)
        if notification_obj is not None:
            notification_obj.status = 'inactive'
            notification_obj.save()
            return Response({'ack': 'canceled', 'id': friend.id}, status=status.HTTP_200_OK)
        try:
            Notification.objects.create(created_by=user, to_user=friend, notification_body=f'<a href="">{user.first_name} {user.last_name}</a> send you a friend request.')
            return Response({'ack': 'created', 'id': friend.id}, status=status.HTTP_200_OK)
        except:
            return Response({'ack': 'error'}, status=status.HTTP_400_BAD_REQUEST)
