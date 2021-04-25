from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q

from account.serializers import UserSerializer
from .serializers import MessageSerializer
from .models import Message, Thread


class ChatIndexView(View):
    template_name = 'chat/chatroom.html'

    def get_chats(self, me, friend):
        thread_obj = None
        try:
            thread_obj = Thread.objects.get((Q(user1=me) & Q(user2=friend)) | (Q(user1=friend) & Q(user2=me)))
            return Message.objects.order_by('timestamp').filter(thread=thread_obj)
        except:
            return None

    def get(self, request, friend):
        user = request.user
        context = {}
        if user.is_authenticated and user.is_superuser==False:
            serialized_data = UserSerializer(user)
            friend_obj = User.objects.get(username=friend)
            friend_serialized_data = UserSerializer(friend_obj)

            all_chats = self.get_chats(user, friend_obj)
            if all_chats is not None:
                chat_serialized_data = MessageSerializer(all_chats, many=True)
                context = {
                    'me': serialized_data.data,
                    'friend': friend_serialized_data.data,
                    'chats': chat_serialized_data.data
                }
            else:
                context = {
                    'me': serialized_data.data,
                    'friend': friend_serialized_data.data,
                    'chats': ''
                }    
            
            return render(request, self.template_name, context)
        return redirect('login')


