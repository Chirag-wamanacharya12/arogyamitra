import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a backup of the database'

    def handle(self, *args, **kwargs):
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')

        os.system(f'python manage.py dumpdata > "{backup_file}"')

        self.stdout.write(self.style.SUCCESS(f'Database backup created: {backup_file}'))
