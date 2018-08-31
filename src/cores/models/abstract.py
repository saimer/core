from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.formats import localize

EMPTY_VALUE_DISPLAY = '---'

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
        ordering = ['-created', ]

    def admin_created(self):
        """
        Return admin display created.
        """
        if self.created_by:
            return format_html(
                mark_safe("{}<br /> {}".format(
                    self.created_by,
                    localize(self.created).replace(" ", "<br />", 1)
                ))
            )
        else:
            return format_html(
                mark_safe("{}".format(
                    localize(self.created).replace(" ", "<br />", 1)
                ))
            )
    admin_created.admin_order_field = 'created'
    admin_created.short_description = 'Created'

    def admin_modified(self):
        """
        Return admin display modified.
        """
        if self.modified_by:
            return format_html(
                mark_safe("{}<br /> {}".format(
                    self.modified_by,
                    localize(self.modified).replace(" ", "<br />", 1)
                ))
            )
        else:
            return EMPTY_VALUE_DISPLAY

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
                    field.value_from_object(self) or EMPTY_VALUE_DISPLAY
                )


class AbstractOrderableModel(models.Model):
    """
    An abstract model that provides orderable function
    based on `ordering` fields.
    """
    sort_order = models.IntegerField(
        verbose_name=_("Ordering"),
        blank=True, null=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['sort_order', ]

    def save(self, *args, **kwargs):
        model = self.__class__

        # Auto calculate sort_order
        if self.sort_order is None:
            try:
                last = model.objects.order_by('-sort_order')[0]
                self.sort_order = last.sort_order + 1
            except IndexError:
                # This item is first row
                self.sort_order = 1

        super().save(*args, **kwargs)
