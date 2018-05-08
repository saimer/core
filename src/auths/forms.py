from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from cores.forms import FormMixin, CoreModelForm


UserModel = get_user_model()


class LoginForm(FormMixin, AuthenticationForm):
    remember_me = forms.BooleanField(
        label=_("Remember me"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'custom-control-input'}
        )
    )


class UserForm(CoreModelForm):

    class Meta:
        model = UserModel
        fields = [
            'avatar', 'first_name', 'last_name',
            'email', 'ic', 'address', 'phone',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            if key not in ['avatar']:
                self.fields[key].required = True
