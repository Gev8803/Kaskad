"""WSGI config for the Kaskad Group CMS."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaskad_cms.settings")

application = get_wsgi_application()
