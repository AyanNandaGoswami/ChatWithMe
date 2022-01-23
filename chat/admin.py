from django.contrib import admin

from .models import *

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'timestamp')
    search_fields = ['room_name', 'unique_room_id']

admin.site.register(Thread, ThreadAdmin)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'messag_body', 'from_user', 'to_user', 'thread', 'timestamp']
    readonly_fields = ['messag_body', 'from_user', 'to_user', 'thread', 'timestamp']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'notification_body', 'notification_type', 'created_by', 'to_user', 'created_at']

