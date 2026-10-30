import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# On Vercel: collect static files + run migrations once at cold start
if os.getenv("VERCEL") == "1":
    try:
        from django.core.management import call_command
        call_command("collectstatic", "--noinput", verbosity=0)
    except Exception as e:
        print("COLLECTSTATIC WARNING:", e)

    if os.getenv("DATABASE_URL"):
        try:
            from django.core.management import call_command
            call_command("migrate", "--noinput", verbosity=0)
        except Exception as e:
            print("MIGRATE WARNING:", e)

application = get_wsgi_application()
