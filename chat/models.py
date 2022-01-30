from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.db.models import Q


class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_one')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_two')
    unique_room_id = models.CharField(max_length=10, null=True, blank=True)
    room_name = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def create_new_room(self):
        self.room_name = f'{self.user1.username}-{self.unique_room_id}-{self.user2.username}'
        self.save()

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        ordering = ['-timestamp']    

def unique_room_id_generator(sender, instance, *args, **kwargs):
    from ChatWithMe.custom_functions import unique_room_genarator
    if not instance.unique_room_id:
        instance.unique_room_id = unique_room_genarator(instance)

pre_save.connect(unique_room_id_generator, sender=Thread)

@receiver(post_save, sender=Thread)
def create_room_name(sender, instance, created, **kwargs):
    if created:
        instance.create_new_room()


class Message(models.Model):
    messag_body = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

@receiver(post_save, sender=Message)
def _message_post_save_receiver(sender, created, instance, **kwargs):
    if created:
        from .helpers import enable_socket_notification_to_user
        # trigger websocket for to_user
        queryset = Notification.objects.order_by('-id').filter(Q(to_user__id=instance.to_user.id) & Q(status__exact="active"))
        enable_socket_notification_to_user(instance.to_user, queryset, True, False)        
        # trigger websocket for from_user
        queryset = Notification.objects.order_by('-id').filter(Q(to_user__id=instance.from_user.id) & Q(status__exact="active"))
        enable_socket_notification_to_user(instance.from_user, queryset, True, False)



class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('accept_or_reject', 'Accept or Reject Friend Request'),
        ('send', 'Send Friend Request'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    status = models.CharField(max_length=9, default='active', choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_created_by', blank=True, null=True)
    notification_body = RichTextField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to_user', blank=True, null=True)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES, default='send')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_body

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-id', ]

@receiver(post_save, sender=Notification)
def _post_save_receiver(sender, created, instance, **kwargs):
    from .helpers import enable_socket_notification_to_user
    queryset = Notification.objects.order_by('-id').filter(Q(to_user__id=instance.to_user.id) & Q(status__exact="active"))
    if created:
        enable_socket_notification_to_user(instance.to_user, queryset, False, True)
    else:
        enable_socket_notification_to_user(instance.to_user, queryset, False, False)

