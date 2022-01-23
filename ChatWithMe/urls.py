"""ChatWithMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from home.views import IndexView
from account.views import LoginView, RegisterView, ProfileView, SearchuserView
from account.api import LogoutAPI
from chat.views import ChatIndexView
from home.views import showFirebaseJS


urlpatterns = [
    path('admin/', admin.site.urls),
    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('search/', SearchuserView.as_view(), name='search'),
    path('chatroom/<str:friend>/', ChatIndexView.as_view(), name='chatroom'),
    path('account/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

