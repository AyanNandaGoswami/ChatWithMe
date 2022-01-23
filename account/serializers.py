from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from .models import FriendList
from chat.models import Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password', 'id']
         # password will not be render with the user
        extra_kwargs = {'password': {'write_only': True}}
    
    # override create method for password hashing
    def create(self, validated_data):

        user = User(
            username= validated_data['username'],
            email= validated_data['email'],
            first_name= validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FriendSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    friends = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = FriendList
        fields = '__all__'


class AcceptRejectSerializer(serializers.Serializer):
    notification_id = serializers.IntegerField()
    action = serializers.CharField()

    def validate(self, attrs):
        try:
            notifi_obj = Notification.objects.get(id=attrs['notification_id'])
        except:
            raise exceptions.NotFound(f'Notification id {attrs["notification_id"]} does not exists.')

        if attrs['action'] != 'accepted' and attrs['action'] != 'rejected':
            raise exceptions.ValidationError(f'{attrs["action"]} is not a valid action.')
        res = {
            'notification_obj': notifi_obj,
            'action': attrs['action']
        }
        return res


class UnfriendSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    friend = serializers.IntegerField()

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs['user'])
        except:
            raise exceptions.NotFound(f'User id {attrs["user"]} does not exists.')

        try:
            friend = User.objects.get(id=attrs['friend'])
        except:
            raise exceptions.NotFound(f'User id {attrs["friend"]} does not exists.')

        res = {
            'user': user,
            'friend': friend
        }
        return res


