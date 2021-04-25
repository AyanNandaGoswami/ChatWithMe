from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request):
        auth = False
        user = request.user
        if user.is_authenticated and user.is_superuser==False:
            auth = True
        return render(request, self.template_name, {'status': auth})



