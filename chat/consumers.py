from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q
from asgiref.sync import sync_to_async, async_to_sync
import json
from chat.models import Thread, Message, Notification
from account.serializers import UserSerializer
from .serializers import NotificationSerializer
from .helpers import get_friend_list_with_last_message


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        friend = None

        me = self.scope['user']     # logged in user
        friend_name = self.scope['url_route']['kwargs']['friend']   # get the username of that user, whoom you want to chat

        friend_instance = await sync_to_async(User.objects.get, thread_sensitive=True)(username=friend_name)    # get user object of friend

        # create a new Thread object if thread of specific chat does not exists, otherwise return the thread
        thread = None
        try:
            thread = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=me) & Q(user2=friend_instance)) | (Q(user1=friend_instance) & Q(user2=me)))
        except:
            thread = await sync_to_async(Thread.objects.create, thread_sensitive=True)(user1=me, user2=friend_instance)

        self.room_name = thread.room_name   # room name

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        '''
            disconnect the websocket connection.
        '''
        await self.channel_layer.group_discard (
            self.room_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        from_user = text_data_json['user']
        to_user = text_data_json['friend']

        from_user_instanse = await sync_to_async(User.objects.get, thread_sensitive=True)(username=from_user['username'])    # get user object of friend
        to_user_instanse = await sync_to_async(User.objects.get, thread_sensitive=True)(username=to_user['username'])    # get user object of friend

        thread_obj = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=from_user_instanse) & Q(user2=to_user_instanse)) | (Q(user1=to_user_instanse) & Q(user2=from_user_instanse)))

        message_instane = await sync_to_async(Message.objects.create, thread_sensitive=True)(messag_body=message, from_user=from_user_instanse, to_user=to_user_instanse, thread=thread_obj)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chatroom_messages',
                'message': message_instane.messag_body,
                'user': message_instane.from_user
            }
        )


    async def chatroom_messages(self, event):
        message = event['message']
        user = event['user']

        user_serialized_data = UserSerializer(user)

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user_serialized_data.data
        })) 


class NotificationConsumer(WebsocketConsumer):
    def connect(self, *args, **kwargs):
        print('connect')
        user = self.scope['url_route']['kwargs']['user_id']
        room_name = user + '_notification'
        room_group_name = 'room_%s' % room_name
        queryset = Notification.objects.filter(Q(to_user__id=user) & Q(status__exact="active"))
        serializer = NotificationSerializer(queryset, many=True)
        async_to_sync(self.channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )
        friends = get_friend_list_with_last_message(user)
        self.accept()
        self.send(
            json.dumps({'notifications': serializer.data, 'friends': friends})
        )

    def disconnect(self, close_code):
        user = self.scope['url_route']['kwargs']['user_id']
        room_name = user + '_notification'
        room_group_name = 'room_%s' % room_name
        self.channel_layer.group_discard (
            room_group_name,
            self.channel_name
        )

    def send_notification(self, event):
        serializer = NotificationSerializer(event['queryset'], many=event['many'])
        friends = get_friend_list_with_last_message(event['user'])

        if event['many'] is False:
            res = {
                'notifications': [serializer.data],
                'friends': friends
            }
        else:
            res = {
                'notifications': serializer.data,
                'friends': friends
            }

        self.send(
            json.dumps(res)
        )


