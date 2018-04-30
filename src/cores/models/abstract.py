from django.db import models
from django.utils.timezone import localtime
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail import ImageField


EXCLUDE_FIELDS = [
    'id', 'slug', 'created_by', 'modified_by', 'created', 'modified',
]


class AbstractTimeStampedModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created`` and ``modified`` fields.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name='+',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Modified by"),
        related_name='+',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    created = models.DateTimeField(
        verbose_name=_("Created date"), auto_now_add=True
    )
    modified = models.DateTimeField(
        verbose_name=_("Modified date"), auto_now=True
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'

    def admin_created(self):
        """
        Return admin display created.
        """
        if self.created_by:
            return format_html(
                mark_safe("{}<br /> {}".format(
                    self.created_by, localtime(self.created).strftime(
                        "%Y-%m-%d<br /> %I:%M %p"
                    )
                ))
            )
        else:
            return '-'

    admin_created.admin_order_field = 'created'
    admin_created.short_description = 'Created'

    def admin_modified(self):
        """
        Return admin display modified.
        """
        if self.modified_by:
            return format_html(
                mark_safe("{}<br /> {}".format(
                    self.modified_by, localtime(self.modified).strftime(
                        "%Y-%m-%d<br /> %I:%M %p"
                    )
                ))
            )
        else:
            return '-'

    admin_modified.admin_order_field = 'modified'
    admin_modified.short_description = 'Modified'

    def display_fields(self):
        """
        Use to display all fields on template.
        """
        for field in self._meta.fields:
            if field.name not in EXCLUDE_FIELDS:
                yield (
                    field.verbose_name.title(),
                    field.value_from_object(self) or '-'
                )


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
