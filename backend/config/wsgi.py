"""WSGI entry point gunicorn serves in production."""

import os

from django.core.wsgi import get_wsgi_application

# Default settings module unless the environment overrides it
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
