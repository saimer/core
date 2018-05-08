from django.apps import AppConfig


class AuthsConfig(AppConfig):
    name = 'auths'

    def ready(self):
        from .signals import (
            auto_delete_avatar_on_delete,
            auto_delete_avatar_on_change
        )
