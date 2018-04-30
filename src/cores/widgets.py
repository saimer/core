import logging
import os
from PIL import Image

from django import forms
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy

from sorl.thumbnail.shortcuts import get_thumbnail


logger = logging.getLogger(__name__)


class CoreAdminImageWidget(forms.ClearableFileInput):
    """
    An ImageField Widget for django.contrib.admin that shows a thumbnailed
    image as well as a link to the current one if it hase one.
    """

    def render(self, name, value, attrs=None):
        output = super().render(name, value, attrs)

        if value and hasattr(value, 'url'):
            ext = 'JPEG'
            try:
                aux_ext = str(value).split('.')
                if aux_ext[len(aux_ext) - 1].lower() == 'png':
                    ext = 'PNG'
                elif aux_ext[len(aux_ext) - 1].lower() == 'gif':
                    ext = 'GIF'
            except Exception:
                pass
            try:
                mini = get_thumbnail(value, 'x80', upscale=False, format=ext)
            except Exception as e:
                logger.warning("Unable to get the thumbnail", exc_info=e)
            else:
                try:
                    output = (
                        '<div style="float:left">'
                        '<a style="width:%spx; display:block; margin:0 0 10px; '
                        'border:1px solid #CCC;" class="thumbnail" '
                        'target="_blank" href="%s">'
                        '<img src="%s"></a>%s</div>'
                    ) % (mini.width, value.url, mini.url, output)
                except (AttributeError, TypeError):
                    pass
        return mark_safe(output)


class CoreImageWidget(forms.ClearableFileInput):
    """
    An ImageField Widget shows a thumbnailed image as well as
    a link to the current one if it hase one.
    """
    clear_checkbox_label = gettext_lazy('Remove this file')
    template_name = 'wanpow/widgets/clearable_file_input.html'

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)

        if value and hasattr(value, 'url'):
            try:
                Image.open(value)
            except OSError:
                context['thumb_img'] = None
                context['filename'] = os.path.basename(value.name)
            else:
                ext = 'JPEG'
                try:
                    aux_ext = str(value).split('.')
                    if aux_ext[len(aux_ext) - 1].lower() == 'png':
                        ext = 'PNG'
                except Exception:
                    pass

                try:
                    mini = get_thumbnail(value, 'x100', upscale=False, format=ext)
                except Exception as e:
                    logger.warn("Unable to get the thumbnail", exc_info=e)
                else:
                    context['thumb_img'] = mini
                    context['filename'] = os.path.basename(value.name)

        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
