from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, FriendRequest, CustomUser

@receiver(post_save, sender=FriendRequest)
def create_friend_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.to_user,
            notification_type='friend_request',

        )
