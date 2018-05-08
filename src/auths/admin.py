from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from cores.admin import AdminImageMixin


UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(AdminImageMixin, BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_("Personal info"), {
            'fields': (
                'avatar', 'first_name', 'last_name', 'email',
                'ic', 'address', 'phone'
            )
        }),
        (_("Permissions"), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        (_("Important dates"), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'username', 'get_groups', 'email', 'get_avatar_thumb',
        'first_name', 'last_name', 'ic', 'phone', 'is_staff'
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'ic')
