from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse


class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request):
        auth = False
        user = request.user
        if user.is_authenticated and user.is_superuser==False:
            auth = True
        return render(request, self.template_name, {'status': auth})


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/9.6.2/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/9.6.2/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCtzO9tXSnWmmH4df3m0EQPAwpu6DP_y6o",' \
         '        authDomain: "push-noti-aff53.firebaseapp.com",' \
         '        projectId: "push-noti-aff53,' \
         '        storageBucket: "push-noti-aff53.appspot.com",' \
         '        messagingSenderId: "978127399610",' \
         '        appId: "1:978127399610:web:c69c1bd4026d01d3a1b083",' \
         '        measurementId: "G-NY05LLW5PY"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")


