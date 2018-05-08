from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core import management


UserModel = get_user_model()


class UserCreationTestCase(TestCase):
    """
    Test case to create user.
    """

    def test_user_creation(self):
        """
        Testing to create a user.

        Expected result:
        - User created successfully
        """
        user = UserModel.objects.create_user(
            username="saimer"
        )
        self.assertEqual(user.email, "")
        self.assertEqual(user.username, "saimer")
        self.assertFalse(user.has_usable_password())

    def test_user_recreate(self):
        """
        Testing to re-create same user.

        Expected result:
        - Raise exception IntegrityError
        """
        self.test_user_creation()

        with self.assertRaisesMessage(
            IntegrityError, "UNIQUE constraint failed: auths_user.username"
        ):
            UserModel.objects.create_user(
                username="saimer"
            )

    def test_user_command_createsuperadmin(self):
        """
        Testing to call custom command createsuperadmin.

        Expected result:
        - Superadmin created successfully
        """
        management.call_command('createsuperadmin', '--force')
        user = UserModel.objects.get(
            username="admin"
        )
        self.assertEqual(user.email, "saimer@snapdec.com")
        self.assertEqual(user.username, "admin")
