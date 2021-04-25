from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse

from .serializers import UserSerializer
from .models import FriendList


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
        context = {}
        if user.is_authenticated and user.is_superuser==False:
            serialized_data = UserSerializer(user)
            friend_list = FriendList.objects.filter(user=user)
            for i in friend_list:
                friend_list = i.friends.all()
            return render(request, self.template_name, {'friends': friend_list, 'logged_in_user': serialized_data.data})
        return redirect('login')


class SearchuserView(View):
    template_name = 'account/search-result-user.html'

    def post(self, request):
        users = User.objects.filter(first_name__icontains=request.POST['query'])
        user = request.user
        serialized_data = UserSerializer(user)
        if users:
            context = {
                'users': users,
                'logged_in_user': serialized_data.data
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponse('No user\'s found with this query.')
