from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from sorl.thumbnail.shortcuts import get_thumbnail

from ..managers import UserManager

from .abstract import AbstractBasicProfileModel


class User(AbstractUser, AbstractBasicProfileModel):
    """
    User model.
    """

    objects = UserManager()

    def get_groups(self):
        return format_html(
            '<br />'.join([x.name for x in self.groups.all()])
        )

    get_groups.short_description = _("Groups")

    def get_avatar_thumb(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            ext = 'JPEG'
            try:
                aux_ext = str(self.avatar).split('.')
                if aux_ext[len(aux_ext) - 1].lower() == 'png':
                    ext = 'PNG'
            except Exception:
                pass

            thumb = get_thumbnail(self.avatar, 'x36', upscale=False, format=ext)
            return mark_safe('<img width="{}" height={} src="{}" />'.format(thumb.width, thumb.height, thumb.url))
        else:
            return mark_safe("-")

    get_avatar_thumb.short_description = _("Profile image")
