from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


UserModel = get_user_model()


class Command(BaseCommand):
    """
    Command to create superadmin for the system
    """
    help = "Use to create a superadmin."

    def add_arguments(self, parser):
        # --commit (optional) arguments
        parser.add_argument(
            '--force',
            '-f',
            action='store_true',
            dest='force',
            default=False,
            help="Force change",
        )
        parser.add_argument(
            '--username',
            '-u',
            default='admin',
            help="Username for superadmin",
        )
        parser.add_argument(
            '--email',
            '-e',
            default='saimer@snapdec.com',
            help="Email for superadmin",
        )
        parser.add_argument(
            '--pass',
            '-p',
            default='Snapdec2018!',
            help="Password for superadmin",
        )

    def handle(self, *args, **options):
        if options['force']:
            user_input = str()
        else:
            user_input = input(
                "Are you sure you want to create a superadmin?\n"
                "- username: {} \n- email: {} \n(Y/N) ".format(
                    options['username'],
                    options['email'],
                )
            )

        if user_input.lower() == "y" or options['force']:
            if UserModel.objects.filter(username=options['username']).exists():
                self.stdout.write(
                    self.style.ERROR(
                        "Superadmin with username `{}` already exist.".format(
                            options['username']
                        )
                    )
                )
            else:
                user = UserModel.objects.create_superuser(
                    username=options['username'],
                    email=options['email'],
                    password=options['pass']
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully created superadmin `{}`.".format(
                            user.username
                        )
                    )
                )
