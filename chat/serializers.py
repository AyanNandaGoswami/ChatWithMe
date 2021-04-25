from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(many=False)
    to_user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Message
        fields = '__all__'

