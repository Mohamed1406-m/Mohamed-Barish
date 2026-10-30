import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

if os.getenv("VERCEL") == "1":
    from django.core.management import call_command

    # /tmp is the only writable directory on Vercel
    try:
        call_command("collectstatic", "--noinput", verbosity=0)
    except Exception as e:
        print("COLLECTSTATIC WARNING:", e)

    if os.getenv("DATABASE_URL"):
        try:
            call_command("migrate", "--noinput", verbosity=0)
        except Exception as e:
            print("MIGRATE WARNING:", e)

        # Create superuser if none exists
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(is_superuser=True).exists():
                pwd = os.getenv("ADMIN_PASSWORD", "changeme123")
                User.objects.create_superuser(
                    username="admin",
                    email="mdbarish1502@gmail.com",
                    password=pwd,
                )
                print("Superuser created")
        except Exception as e:
            print("SUPERUSER WARNING:", e)
