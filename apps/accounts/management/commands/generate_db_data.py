from django.core.management.base import BaseCommand
from db_scripts.generate_db_data import generate_fake_db_data

class Command(BaseCommand):
    help = 'Generate test data for the Wind For life database'

    def handle(self, *args, **kwargs):
        generate_fake_db_data()
        self.stdout.write(self.style.SUCCESS('Successfully initialized the database'))