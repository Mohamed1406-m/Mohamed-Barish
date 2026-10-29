# Barish portfolio (Django + Vercel)
Local: pip install -r requirements.txt; copy .env.example values into your shell; python manage.py runserver
Deploy: push to GitHub, import in Vercel, add the env vars from .env.example.
Voice: Vercel cannot run agent.py (long-lived worker). Deploy it on LiveKit Cloud/Render/Railway with the same LiveKit keys.
