from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username='superuser').exists():
            User.objects.create_superuser('superuser', email='', password='superuser')
            print("Superuser created with credentials:\n\tusername: superuser\n\tpassword: superuser")

        else:
            print('Superuser already exists')