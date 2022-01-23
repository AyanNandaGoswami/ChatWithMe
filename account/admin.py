from django.contrib import admin
from .models import FriendList


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


