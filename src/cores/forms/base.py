from django import forms

from .mixins import FormMixin, FormRequestMixin


class CoreForm(FormMixin, FormRequestMixin, forms.Form):
    pass


class CoreModelForm(FormMixin, FormRequestMixin, forms.ModelForm):
    pass
