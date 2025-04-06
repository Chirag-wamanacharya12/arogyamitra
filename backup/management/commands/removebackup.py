import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Remove old database backups'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all', 
            action='store_true', 
            help='Remove all backups'
        )
        parser.add_argument(
            '--latest', 
            action='store_true', 
            help='Remove only the latest backup'
        )

    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')

        if not os.path.exists(backup_dir):
            self.stdout.write(self.style.WARNING("No backups found."))
            return

        backups = sorted(os.listdir(backup_dir), reverse=True)

        if options['all']:
            for backup in backups:
                os.remove(os.path.join(backup_dir, backup))
            self.stdout.write(self.style.SUCCESS("All backups removed successfully."))

        elif options['latest']:
            if backups:
                os.remove(os.path.join(backup_dir, backups[0]))
                self.stdout.write(self.style.SUCCESS(f"Latest backup {backups[0]} removed successfully."))
            else:
                self.stdout.write(self.style.WARNING("No backups to remove."))

        else:
            self.stdout.write(self.style.WARNING("Use --all to remove all backups or --latest to remove the latest one."))
