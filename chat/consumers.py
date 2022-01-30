from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q
from asgiref.sync import sync_to_async, async_to_sync
import json
from chat.models import Thread, Message, Notification
from account.serializers import UserSerializer
from .serializers import NotificationSerializer
from .helpers import get_friend_list_with_last_message
from channels.layers import get_channel_layer


class ChatConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def get_message_queryset(self, thread):
        try:
            return list(Message.objects.all().filter(thread=thread).update(is_read=True))
        except:
            pass

    async def connect(self):
        user = self.scope['user']     # logged in user
        friend = await sync_to_async(User.objects.get, thread_sensitive=True)(username=self.scope['url_route']['kwargs']['friend'])    # get user object of friend

        # create a new Thread object if thread of specific chat does not exists, otherwise return the thread
        thread = None
        try:
            thread = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=user) & Q(user2=friend)) | (Q(user1=friend) & Q(user2=user)))
        except:
            thread = await sync_to_async(Thread.objects.create, thread_sensitive=True)(user1=user, user2=friend)
        finally:
            self.room_name = thread.room_name   # room name

        await self.get_message_queryset(thread) # update is_read property to true of messages

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
        payload = json.loads(text_data)
        from_user = await sync_to_async(User.objects.get, thread_sensitive=True)(username=payload['user']['username'])    # get user object of friend
        to_user = await sync_to_async(User.objects.get, thread_sensitive=True)(username=payload['friend']['username'])    # get user object of friend

        thread_obj = await sync_to_async(Thread.objects.get, thread_sensitive=True)((Q(user1=from_user) & Q(user2=to_user)) | (Q(user1=to_user) & Q(user2=from_user)))

        message_instane = await sync_to_async(Message.objects.create, thread_sensitive=True)(messag_body=payload['message'], from_user=from_user, to_user=to_user, thread=thread_obj)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chatroom_messages',
                'message': message_instane.messag_body,
                'user': message_instane.from_user
            }
        )

    async def chatroom_messages(self, event):
        user_serialized_data = UserSerializer(event['user'])

        await self.send(text_data=json.dumps({
            'message': event['message'],
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
                'friends': friends,
                'chat_created': event['chat_created'],
                'noti_created': event['noti_created']
            }
        else:
            res = {
                'notifications': serializer.data,
                'friends': friends,
                'chat_created': event['chat_created'],
                'noti_created': event['noti_created']
            }

        self.send(
            json.dumps(res)
        )




# class ChatConsumer(WebsocketConsumer):
    
#     def connect(self):
#         user = self.scope['user']     # logged in user
#         friend = User.objects.get(username=self.scope['url_route']['kwargs']['friend'])    # get user object of friend

#         # create a new Thread object if thread of specific chat does not exists, otherwise return the thread
#         thread = None
#         try:
#             thread = Thread.objects.get((Q(user1=user) & Q(user2=friend)) | ((Q(user1=friend) & Q(user2=user))))
#         except:
#             thread = Thread.objects.create(user1=user, user2=friend)
#         finally:
#             self.room_name = thread.room_name   # room name

#         # update is_read property
#         # message_queryset = Message.objects.filter(Q(thread__id=thread.id))
#         # print(message_queryset)

#         self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )

#         self.accept()


#     def disconnect(self, close_code):
#         '''
#         disconnect the websocket connection form chat page
#         '''
#         self.channel_layer.group_discard (
#             self.room_name,
#             self.channel_name
#         )


#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         from_user = text_data_json['user']
#         to_user = text_data_json['friend']

#         from_user_instanse = User.objects.get(username=from_user['username'])    # get user object of friend
#         to_user_instanse = User.objects.get(username=to_user['username'])    # get user object of friend

#         thread_obj = Thread.objects.get((Q(user1=from_user_instanse) & Q(user2=to_user_instanse)) | (Q(user1=to_user_instanse) & Q(user2=from_user_instanse)))
#         print(thread_obj)
#         message_instane = Message.objects.create(messag_body=message, from_user=from_user_instanse, to_user=to_user_instanse, thread=thread_obj)
#         print(message_instane)

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_name,
#             {
#                 'type': 'chatroom_messages',
#                 'message': message_instane.messag_body,
#                 'user': message_instane.from_user
#             }
#         )


#     def chatroom_messages(self, event):
#         # Receive message from room group
#         message = event['message']
#         user = event['user']

#         user_serialized_data = UserSerializer(user)
        
#         self.send(text_data=json.dumps({
#             'message': message,
#             'user': user_serialized_data.data
#         })) 
