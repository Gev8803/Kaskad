"""
URL configuration for the Kaskad Group CMS.

Routes:
  /admin/     -> Django admin (the CMS)
  /api/       -> JSON content API consumed by the frontend
  /media/     -> uploaded, optimised images
  /           -> the existing static frontend in `site/`  (dev convenience)

In production you would typically serve `site/` and `/media` with nginx or a
CDN; the catch-all frontend server below keeps a single `runserver` fully
working for local development and demos.
"""
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import Http404, HttpResponse
from django.urls import include, path, re_path
from django.views.static import serve as static_serve

admin.site.site_header = "Kaskad Group — Content Management"
admin.site.site_title = "Kaskad Group CMS"
admin.site.index_title = "Manage website content"


def serve_frontend(request, path=""):
    """Serve files from the existing `site/` directory (index.html by default)."""
    rel = path or "index.html"
    full = (settings.SITE_DIR / rel).resolve()
    # Prevent path traversal outside SITE_DIR
    try:
        full.relative_to(settings.SITE_DIR.resolve())
    except ValueError:
        raise Http404("Not found")
    if full.is_dir():
        full = full / "index.html"
        rel = str(Path(rel) / "index.html")
    if not full.exists():
        raise Http404("Not found")
    return static_serve(request, rel, document_root=str(settings.SITE_DIR))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("content.urls")),
    path("healthz", lambda r: HttpResponse("ok")),
]

# Media files (served by Django in dev; nginx/CDN in prod)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Frontend catch-all (kept last so /admin, /api, /media win first)
urlpatterns += [
    re_path(r"^$", serve_frontend, name="frontend-index"),
    re_path(r"^(?P<path>(?!admin/|api/|media/|static/).*)$", serve_frontend),
]
