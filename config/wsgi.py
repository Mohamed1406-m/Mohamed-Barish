import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

# Auto-migrate on Vercel when a real DB is connected
if os.getenv("DATABASE_URL"):
    try:
        from django.db import connection
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        if executor.migration_plan(executor.loader.graph.leaf_nodes()):
            from django.core.management import call_command
            call_command("migrate", "--noinput", verbosity=0)
    except Exception as e:
        print("MIGRATE WARNING:", e)
