from django.urls import path
from .apis import UpdateNotificationIsReadValue


urlpatterns = [
    path('chnage-notification-status/', UpdateNotificationIsReadValue.as_view()),
]


