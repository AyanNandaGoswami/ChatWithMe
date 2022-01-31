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
         '        apiKey: "",' \
         '        authDomain: "",' \
         '        projectId: ",' \
         '        storageBucket: "",' \
         '        messagingSenderId: "",' \
         '        appId: "",' \
         '        measurementId: ""' \
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


