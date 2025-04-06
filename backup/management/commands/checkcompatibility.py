from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = "Check if all required tables exist in the database"

    def handle(self, *args, **options):
        # 🔍 Step 1: Fetch all user-created apps (ignore Django default apps)
        user_apps = [app.label for app in apps.get_app_configs() if not app.label.startswith('django')]

        # 🔍 Step 2: Get required table names from Django models
        required_tables = set()
        for app_label in user_apps:
            models = apps.get_app_config(app_label).get_models()
            for model in models:
                required_tables.add(model._meta.db_table.lower())  # Ensure lowercase

        # 🔍 Step 3: Fetch actual table names from the database
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            existing_tables = {row[0].lower() for row in cursor.fetchall()}  # Ensure lowercase

        # 🔍 Step 4: Compare required vs. existing tables
        missing_tables = required_tables - existing_tables

        if missing_tables:
            self.stdout.write(self.style.ERROR("❌ Missing Tables:"))
            for table in missing_tables:
                self.stdout.write(f"   - {table}")
        else:
            self.stdout.write(self.style.SUCCESS("✅ All required tables are present!"))
