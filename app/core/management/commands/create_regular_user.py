""" 
Command to create regular user - to be as a convinient solution for task reviewer.
"""

from core.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        password = "password"
        email = "user@example.com"
        name = "test_user"

        # If user exist.
        if User.objects.filter(email=email):
            return

        User.objects.create_user(
            name=name, email=email, password=password
        )

        self.stdout.write(
            f'Local regular user with email: "{email}" was created'
        )
