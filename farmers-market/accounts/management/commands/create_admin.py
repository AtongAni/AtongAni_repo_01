from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='Admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@farmersmarket.com', help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Admin user '{username}' already exists!")
            )
            return

        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role=User.Role.ADMIN
        )

        self.stdout.write(
            self.style.SUCCESS(f"Admin user '{username}' created successfully!")
        )
        self.stdout.write(f"Email: {email}")
        self.stdout.write(f"Password: {password}")
