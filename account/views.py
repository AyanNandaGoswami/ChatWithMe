from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.db.models import Q

from .serializers import UserSerializer
from .models import FriendList
from chat.models import Notification, Message


class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated and user.is_superuser==False:
            return redirect('profile')
        return render(request, self.template_name)
        

class ProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated and user.is_superuser==False:
            serialized_data = UserSerializer(user)
            return render(request, self.template_name, {'logged_in_user': serialized_data.data})
        return redirect('login')


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


