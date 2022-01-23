from .models import Notification
from .serializers import NotificationSerializer


def create_new_notification(data):
    serializer = NotificationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return True
    print(serializer.errors)
    return False


