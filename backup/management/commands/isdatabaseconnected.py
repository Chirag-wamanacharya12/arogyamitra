from django.core.management.base import BaseCommand
from django.db import connection, OperationalError, DatabaseError
from django.conf import settings

class Command(BaseCommand):
    help = 'Check if the database is connected to the Django project'

    def handle(self, *args, **options):
        db_config = settings.DATABASES.get('default', {})
        db_name = db_config.get('NAME', 'Unknown Database')
        db_engine = db_config.get('ENGINE', 'Unknown Engine')
        db_user = db_config.get('USER', 'Unknown User')
        db_host = db_config.get('HOST', 'Unknown Host')
        db_port = db_config.get('PORT', 'Unknown Port')

        self.stdout.write(f"🔍 Checking connection to database: {db_name} (Engine: {db_engine})")

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")  # Test query

            self.stdout.write(self.style.SUCCESS(f"✅ Database '{db_name}' is successfully connected!"))
            return

        except OperationalError as e:
            error_msg = str(e).lower()

            # 🛑 Handling specific MySQL errors based on your scenario
            if "unknown database" in error_msg:
                reason = f"❌ The database '{db_name}' does not exist. Please check database name or create it before connecting."
            elif "access denied" in error_msg:
                reason = f"❌ Access denied for user '{db_user}'. Check username or password."
            elif "could not connect" in error_msg or "connection refused" in error_msg:
                reason = f"❌ Cannot connect to MySQL at {db_host}:{db_port}. Ensure the server is running."
            elif "no such table" in error_msg:
                reason = f"❌ The database '{db_name}' exists, but required tables are missing."
            elif "server has gone away" in error_msg:
                reason = f"❌ MySQL server at {db_host}:{db_port} is unreachable. Restart the database service."
            else:
                reason = f"❌ Unexpected database error: {str(e)}"

        except DatabaseError as e:
            reason = f"❌ General database error: {str(e)}"

        except Exception as e:
            reason = f"❌ Unknown error: {str(e)}"

        # 🛑 Display human-readable error message
        self.stdout.write(self.style.ERROR(reason))
