from django.urls import path

from .api import *
from .views import *

urlpatterns = [
    path('create-new-user/', CreateUserAPI.as_view(), name='create_new_user'),
    path('user-login/', LoginAPi.as_view(), name='user_login'),
    path('add-to-list/', CreateFriendAPI.as_view(), name='add_tp_list'),
    path('remove-from-list/', RemoveFriendAPI.as_view(), name='remover_from_list'),
]

