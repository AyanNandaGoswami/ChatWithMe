from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models import Q

from .serializers import UserSerializer
from .models import FriendList
from chat.models import Notification, Message
from asgiref.sync import async_to_sync
from communication.auth_service_request import get_data_from_nats
from utils.constants.base import AUTH_TOKEN


class ChatContactsListsView(View):
    """
    this view is to handle the recent-chat/chat-contacts screen for logged-in user
    """
    template_name: str = 'chat/recent_chat.html'

    def get(self, request):
        # retrieve the access token stored in COOKIES
        access_token: str = request.COOKIES.get(AUTH_TOKEN)
        if not access_token:
            redirect('/')
        # call the async NATS handler to fetch the user_information against the access token
        response = async_to_sync(get_data_from_nats)({
            "access_token": access_token
        })
        return render(request, self.template_name, {'user': response})


class SearchuserView(View):
    template_name = 'account/search-result-user.html'

    def post(self, request):
        friend_flag_list = []
        request_flag_list = []
        queryset = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(full_name__icontains=request.POST['query'])
        friend_obj = FriendList.objects.filter(user=request.user).last()
        if friend_obj is not None:
            for i in queryset:
                friend_flag_list.append(True) if friend_obj.friends.filter(pk=i.id) else friend_flag_list.append(False)
                request_flag_list.append(False) if Notification.objects.filter(Q(created_by=request.user) & Q(to_user=i) & Q(status__exact='active') & Q(notification_type__exact='send')).last() is None else request_flag_list.append(True)
        else:
            for i in queryset:
                friend_flag_list.append(False)
                request_flag_list.append(False) if Notification.objects.filter(Q(created_by=request.user) & Q(to_user=i) & Q(status__exact='active') & Q(notification_type__exact='send')).last() is None else request_flag_list.append(True)

        serialized_data = UserSerializer(request.user)

        if queryset:
            context = {
                'users': zip(queryset, friend_flag_list, request_flag_list),
                'logged_in_user': serialized_data.data,
                'data_found': True
            }
            return render(request, self.template_name, context)
        else:
            context = {
                'data_found': False
            }
            return render(request, self.template_name, context)


