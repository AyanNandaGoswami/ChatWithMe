from django.utils.timezone import localtime
from django.db.models import Q
from account.models import FriendList
from chat.models import Message
from account.serializers import UserSerializer


# def get_friend_list_with_last_message(user):
#     '''
#     This function is used to get friendlist of a user and it also return the last message of each room with timestamp
#     '''
#     queryset = FriendList.objects.filter(user=user)
#     friend_serializeed_data = []
#     time = ''
#     date = ''
#     from_user_ = ''
#     friends = []

#     for i in queryset:
#         for friend in i.friends.all():
#             last_message = Message.objects.filter((Q(from_user=user) & Q(to_user=friend)) | (Q(from_user=friend) & Q(to_user=user))).last()

#             if last_message is not None:
#                 from_user_ = 'Me: ' if last_message.from_user.id == int(user) else f"{last_message.from_user.first_name.split(' ')[0]}: "
#                 date_time = localtime(last_message.timestamp)
#                 time = "%s:%s" % (date_time.hour, date_time.minute)
#                 date = "%s-%s-%s" % (date_time.day, date_time.month, date_time.year)
#                 last_message = last_message.messag_body
#             else:
#                 last_message = ''
#             res = {
#                 **UserSerializer(friend, many=False).data,
#                 **{'last_message': last_message},
#                 **{'time': time},
#                 **{'date': date},
#                 **{'me': from_user_}
#             }
#             friend_serializeed_data.append(res)
#     return friend_serializeed_data






def get_friend_list_with_last_message(user):
    '''
    This function is used to get friendlist of a user and it also return the last message of each room with timestamp
    '''
    friend_list_obj = FriendList.objects.filter(user=user).last()
    friend_serializeed_data = []
    time = ''
    date = ''
    from_user_ = ''
    friends = []
    message_queryset = Message.objects.order_by('-id').filter(Q(from_user=user) |
                                                                        Q(to_user=user))
    for i in message_queryset:
        if (i.from_user.id != int(user)) and (i.from_user not in friends):
            friends.append(i.from_user)
        elif (i.to_user.id != int(user)) and (i.to_user not in friends):
            friends.append(i.to_user)

    for friend in friends:
        if friend_list_obj.friends.filter(id=friend.id).exists():
            last_message = Message.objects.filter((Q(from_user=user) & Q(to_user=friend)) | (Q(from_user=friend) & Q(to_user=user))).last()
            if last_message is not None:
                from_user_ = 'Me: ' if last_message.from_user.id == int(user) else f"{last_message.from_user.first_name.split(' ')[0]}: "
                date_time = localtime(last_message.timestamp)
                time = "%s:%s" % (date_time.hour, date_time.minute)
                date = "%s-%s-%s" % (date_time.day, date_time.month, date_time.year)
                last_message = last_message.messag_body
            else:
                last_message = ''
            res = {
                **UserSerializer(friend, many=False).data,
                **{'last_message': last_message},
                **{'time': time},
                **{'date': date},
                **{'me': from_user_}
            }
            friend_serializeed_data.append(res)
    return friend_serializeed_data

