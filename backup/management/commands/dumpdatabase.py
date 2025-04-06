import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Dump database schema and data'

    def handle(self, *args, **kwargs):
        os.system('python manage.py dbshell < db_dump.sql')
        self.stdout.write(self.style.SUCCESS('Database dumped successfully!'))
