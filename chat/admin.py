from django.contrib import admin

from .models import *

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'timestamp')
    search_fields = ['room_name', 'unique_room_id']

admin.site.register(Thread, ThreadAdmin)


# class MessageAdmin(admin.ModelAdmin):
#     readonly_fields = ['messag_body', 'from_user', 'to_user', 'thread',]

# admin.site.register(Message, MessageAdmin)


admin.site.register(Message)