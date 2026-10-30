import os
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

if os.getenv("VERCEL") == "1":
    import django
    django.setup()
    from django.core.management import call_command

    # /tmp is the only writable dir on Vercel — create it first
    Path("/tmp/staticfiles").mkdir(parents=True, exist_ok=True)

    try:
        call_command("collectstatic", "--noinput", verbosity=0)
    except Exception as e:
        print("COLLECTSTATIC WARNING:", e)

    if os.getenv("DATABASE_URL"):
        try:
            call_command("migrate", "--noinput", verbosity=0)
        except Exception as e:
            print("MIGRATE WARNING:", e)

        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username="admin",
                    email="mdbarish1502@gmail.com",
                    password=os.getenv("ADMIN_PASSWORD", "changeme123"),
                )
                print("Superuser created")
        except Exception as e:
            print("SUPERUSER WARNING:", e)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
