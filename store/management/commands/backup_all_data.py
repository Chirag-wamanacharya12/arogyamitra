import json
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Backup data from all models in all apps to a JSON file'

    def handle(self, *args, **kwargs):
        # Create a dictionary to store data for all models
        data = {}

        # Iterate over all models in all apps
        for model in apps.get_models():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            
            # Fetch all data for the current model and convert it to a list of dictionaries
            data[app_label] = {
                model_name: list(model.objects.values())  # Extract data as a list of dicts
            }

        # Save the data to a JSON file
        with open('full_backup.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS('All models data has been backed up successfully!'))
