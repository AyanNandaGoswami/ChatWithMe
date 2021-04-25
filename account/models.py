from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, related_name='friends')
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friend List'

