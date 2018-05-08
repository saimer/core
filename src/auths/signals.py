import os

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_delete, pre_save


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def auto_delete_avatar_on_delete(sender, instance, **kwargs):
    """
    Deletes avatar from filesystem when User is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def auto_delete_avatar_on_change(sender, instance, **kwargs):
    """
    Deletes old avatar from filesystem when User is updated with new avatar.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_file = instance.avatar
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except Exception:
            return False
