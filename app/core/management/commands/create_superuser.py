""" 
Command to create superuser - to be as a convinient solution for task reviewer.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        # If admin exist.
        if User.objects.exists():
            return

        password = "password"
        email = "admin@example.com"

        User.objects.create_superuser(email=email, password=password)

        self.stdout.write(
            f'Local superuser with email: "{email}" was created'
        )
