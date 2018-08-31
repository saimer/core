from sorl.thumbnail.fields import ImageFormField

from django import forms
from django.utils.formats import get_format

from ..widgets import CoreImageWidget


class FormRequestMixin(object):
    """
    Takes the request from kwargs and pops it into the class attributes
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super().__init__(*args, **kwargs)


class FormMixin(object):
    """
    Mixin for form to add class ``datepicker`` on DateField
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # For custom class
            custom_class = field.widget.attrs.get('class')
            if not custom_class:
                # Set default bootstrap class
                field.widget.attrs['class'] = 'form-control'

            # For Datepicker
            if isinstance(field, forms.DateField) and not custom_class:
                field.widget.attrs['class'] = 'form-control core-datepicker'
                field.widget.attrs['data-date-format'] = \
                    get_format('JS_DATE_INPUT_FORMATS')

            # For Select2
            if (
                (
                    isinstance(field, forms.ChoiceField) or
                    isinstance(field, forms.models.ModelChoiceField)
                ) and
                not custom_class
            ):
                field.widget.attrs['class'] = 'form-control core-select2'

            # For Fileinput
            if (
                (
                    isinstance(field, ImageFormField) or
                    isinstance(field, forms.FileField) or
                    isinstance(field, forms.ClearableFileInput)
                ) and
                not custom_class
            ):
                field.widget = CoreImageWidget(
                    attrs={'class': 'form-control core-fileinput-image'}
                )
