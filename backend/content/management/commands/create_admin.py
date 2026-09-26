"""
Create (or update) the admin superuser from environment variables.

Reads ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD (see settings + .env).
Idempotent: running it again updates the password of the existing user.

    py manage.py create_admin
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create/update the admin superuser from environment variables."

    def handle(self, *args, **options):
        User = get_user_model()
        username = settings.ADMIN_USERNAME
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD

        if not password:
            raise CommandError(
                "ADMIN_PASSWORD is not set. Add it to backend/.env (see .env.example) "
                "or run `py manage.py createsuperuser` interactively instead."
            )

        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email}
        )
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} superuser '{username}'."))
