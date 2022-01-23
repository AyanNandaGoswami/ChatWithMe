from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Message, Notification


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(many=False)
    to_user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

