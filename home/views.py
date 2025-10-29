from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from utils.constants.home import SSO_LOGIN_URL, SSO_REGISTER_URL
from utils.decorators import login_required, inject_user_info


class IndexView(View):
    template_name = 'home/index_new.html'

    def get(self, request):
        logged_in = request.logged_in
        if logged_in:
            return redirect('/options')
        return render(
            request,
            self.template_name,
            {'user_logged_in': logged_in, 'login_url': SSO_LOGIN_URL, 'register_url': SSO_REGISTER_URL}
        )


class OptionsView(View):
    template_name = 'home/options.html'

    @login_required
    @inject_user_info
    def get(self, request, user):
        return render(request, self.template_name, {'user': user})


class PermissionView(View):
    template_name = 'home/permission_manager.html'

    @login_required
    def get(self, request):
        return render(request, self.template_name)


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


