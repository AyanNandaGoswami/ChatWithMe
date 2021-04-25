from rest_framework import serializers

from django.contrib.auth.models import User

from .models import FriendList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password']
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

