import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Ensure static root exists (writable /tmp on Vercel)
if os.getenv("VERCEL") == "1":
    Path("/tmp/staticfiles").mkdir(parents=True, exist_ok=True)

application = get_wsgi_application()
