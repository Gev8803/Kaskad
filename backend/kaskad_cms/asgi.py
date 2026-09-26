"""ASGI config for the Kaskad Group CMS."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaskad_cms.settings")

application = get_asgi_application()
