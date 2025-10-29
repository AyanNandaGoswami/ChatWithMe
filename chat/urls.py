from django.urls import path
from .apis import UpdateNotificationIsReadValue
from .views import ChatListsView

urlpatterns = [
    # page view
    path("list", ChatListsView.as_view(), name="chat_list"),

    # APIs
    path('chnage-notification-status/', UpdateNotificationIsReadValue.as_view()),
]


