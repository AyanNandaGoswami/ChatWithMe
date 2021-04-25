from rest_framework.generics import *
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from .serializers import *
from .models import FriendList


class CreateUserAPI(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        
        if User.objects.filter(email__iexact=data['email']):
            return Response({'username': f'Email {data["email"]} is already taken.'})

        serialized_data = self.serializer_class(data=data)

        if serialized_data.is_valid():
            serialized_data.save()
            username = data['username']
            password = data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
            return Response({'user_deatils': serialized_data.data, 'login': True})
        return Response(serialized_data.errors)


class LoginAPi(GenericAPIView):
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        
        if user and user.is_superuser==False:
            django_login(request, user)
            return Response({'is_authenticated': True}, status=status.HTTP_200_OK)
        return Response({'is_authenticated': False}, status=status.HTTP_200_OK)


class LogoutAPI(GenericAPIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.is_superuser == False:
            django_logout(request)
            return redirect('index')


class CreateFriendAPI(GenericAPIView):
    def post(self, request):
        data = request.data
        friend_obj = None

        user = User.objects.get(username=data['user'])
        friend = User.objects.get(username=data['friend'])

        if FriendList.objects.filter(user=user).exists():
            friend_obj = FriendList.objects.get(user=user)
            friend_obj.friends.add(friend)
        else:
            friend_obj = FriendList.objects.create(user=user)
            friend_obj.friends.add(friend)
                
        if friend_obj is not None:
            return Response({'ack': True}, status=status.HTTP_201_CREATED)


class RemoveFriendAPI(GenericAPIView):
    def post(self, request):
        data = request.data
        friend_obj = None

        user = User.objects.get(username=data['user'])
        friend = User.objects.get(username=data['friend'])

        friend_obj = FriendList.objects.get(user=user)
        friend_obj.friends.remove(friend)

        all_friends = friend_obj.friends.all()
        serialized_data = UserSerializer(all_friends, many=True)

        return Response({'friends': serialized_data.data}, status=status.HTTP_200_OK)



