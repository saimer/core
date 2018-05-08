from django.db import models
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField


class AbstractBasicProfileModel(models.Model):
    """
    Abstract class for basic profile.
    """
    avatar = ImageField(
        verbose_name=_("Profile image"),
        upload_to='avatar',
        blank=True, null=True
    )
    ic = models.CharField(
        verbose_name=_("IC / Passport no."),
        max_length=14,
        blank=True, null=True
    )
    address = models.TextField(
        verbose_name=_("Address"),
        max_length=256,
        blank=True, null=True
    )
    phone = models.CharField(
        verbose_name=_("Phone no."),
        max_length=32,
        blank=True, null=True
    )

    class Meta:
        abstract = True
