from django.urls import path

from .api import *
from .views import *

urlpatterns = [
    path('create-new-user/', CreateUserAPI.as_view(), name='create_new_user'),
    path('user-login/', LoginAPi.as_view(), name='user_login'),
    path('send-friend-request/', SendFriendRequest.as_view(), name='add_tp_list'),
    path('accept-reject-request/', AcceptAndRejectFriendRequestAPI.as_view(), name='accept_and_reject'),
    path('unfriend/', UnfriendAPI.as_view(), name='unfriend'),
]

