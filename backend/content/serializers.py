"""
Serialisation for the Kaskad Group CMS.

`build_content(request)` assembles ONE dict that mirrors the exact global data
shapes the existing frontend consumes:

    { "company": {...},        # -> window.DATA.company
      "construction": {...},   # -> window.DATA.construction
      "switchgear": {...},     # -> window.DATA.switchgear
      "meters": {...},         # -> window.DATA.meters
      "news": [...],           # -> window.DATA.news
      "galleries": {...},      # -> window.DATA.galleries
      "i18n": {hy:{}, ru:{}, en:{}} }  # -> window.I18N

This keeps `site/assets/js/app.js` rendering logic unchanged.
"""
from rest_framework import serializers

from . import models


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _img(request, field):
    """Absolute URL for an image/file field, or None when unset."""
    if not field:
        return None
    try:
        url = field.url
    except ValueError:
        return None
    if request is not None:
        return request.build_absolute_uri(url)
    return url


def _published(qs):
    return qs.filter(is_published=True)


# ---------------------------------------------------------------------------
# company
# ---------------------------------------------------------------------------
def _company(request):
    s = models.SiteSettings.load()
    return {
        "contact": {
            "address": s.tri("address"),
            "phone": s.phone,
            "phoneLink": s.phone_link,
            "email": s.email,
            "mapEmbed": s.map_embed,
        },
        "stats": [
            {"value": x.value, "suffix": x.suffix, "label": x.tri("label")}
            for x in _published(models.Stat.objects.all())
        ],
        "advantages": [
            {"icon": x.icon, "title": x.tri("title"), "text": x.tri("text")}
            for x in _published(models.Advantage.objects.all())
        ],
        "partners": [
            {"name": x.name, "logo": _img(request, x.logo)}
            for x in _published(models.Partner.objects.all())
        ],
        "clients": [
            {"name": x.tri("name"), "logo": _img(request, x.logo)}
            for x in _published(models.Client.objects.all())
        ],
        "values": [
            {"icon": x.icon, "title": x.tri("title"), "text": x.tri("text")}
            for x in _published(models.Value.objects.all())
        ],
        "history": [
            {"year": x.year, "text": x.tri("text")}
            for x in _published(models.HistoryMilestone.objects.all())
        ],
    }


# ---------------------------------------------------------------------------
# construction
# ---------------------------------------------------------------------------
def _construction(request):
    services = []
    for s in _published(models.Service.objects.all().prefetch_related("points")):
        services.append({
            "id": s.slug,
            "icon": s.icon,
            "name": s.tri("name"),
            "summary": s.tri("summary"),
            "points": [p.tri("text") for p in _published(s.points.all())],
        })

    projects = []
    for p in _published(models.Project.objects.all()):
        projects.append({
            "id": p.slug,
            "image": _img(request, p.image),
            "name": p.tri("name"),
            "location": p.tri("location"),
            "country": p.country,
            "year": p.year,
            "category": p.category,
            "client": p.tri("client"),
            "spec": p.spec,
            "description": p.tri("description"),
        })

    categories = [
        {"id": c.slug, "name": c.tri("name")}
        for c in _published(models.ProjectCategory.objects.all())
    ]

    return {
        "services": services,
        "projects": projects,
        "projectCategories": categories,
    }


# ---------------------------------------------------------------------------
# switchgear
# ---------------------------------------------------------------------------
def _sw_item(request, it):
    """Serialise one KD-2 style switchgear module with its full detail."""
    bullets = _published(it.bullets.all())
    def _blist(kind):
        return [b.tri("text") for b in bullets if b.kind == kind]
    out = {
        "code": it.code,
        "name": it.tri("name"),
        "image": _img(request, it.image),
        "description": it.tri("description"),
        "purpose": it.tri("purpose"),
        "gallery": [
            _img(request, g.image) for g in _published(it.gallery.all())
            if _img(request, g.image)
        ],
        "specCols": it.spec_columns(),
        "specs": [
            {
                "param": r.tri("param"),
                "unit": r.unit,
                "values": [r.v1, r.v2, r.v3],
                "group": r.is_group,
            }
            for r in _published(it.spec_rows.all())
        ],
        "notes": it.tri("notes"),
        "equipment": _blist("equipment"),
        "options": _blist("option"),
        "vacuum": _blist("vacuum"),
        "fuse": it.fuse(),
        "pdf": _img(request, it.pdf),
    }
    return out


def _switchgear(request):
    categories = []
    qs = _published(
        models.SwitchgearCategory.objects.all()
        .prefetch_related(
            "items", "items__gallery", "items__bullets", "items__spec_rows",
            "specs", "docs",
        )
    )
    for c in qs:
        entry = {
            "id": c.slug,
            "slug": c.slug,
            "image": _img(request, c.image),
            "voltage": c.voltage or None,
            "current": c.tri("current") if c.current_is_set() else None,
            "name": c.tri("name"),
            "summary": c.tri("summary"),
            "description": c.tri("description"),
            "items": [_sw_item(request, it) for it in _published(c.items.all())],
            "specs": [
                {"label": sp.tri("label"), "value": sp.value()}
                for sp in _published(c.specs.all())
            ],
        }
        docs = [
            {"label": d.tri("label"), "href": _img(request, d.file) or d.href or "#"}
            for d in _published(c.docs.all())
        ]
        if docs:
            entry["docs"] = docs
        categories.append(entry)

    s = models.SiteSettings.load()
    return {
        "categories": categories,
        "manufacturing": s.tri("manufacturing"),
        "certificates": [
            {"title": c.tri("title"), "image": _img(request, c.image)}
            for c in _published(models.Certificate.objects.all())
        ],
    }


# ---------------------------------------------------------------------------
# meters
# ---------------------------------------------------------------------------
def _meters(request):
    categories = [
        {"id": c.slug, "name": c.tri("name")}
        for c in _published(models.MeterCategory.objects.all())
    ]

    products = []
    qs = _published(
        models.Meter.objects.all().select_related("category")
        .prefetch_related("specs", "features")
    )
    for m in qs:
        products.append({
            "id": m.slug,
            "category": m.category.slug,
            "image": _img(request, m.image),
            "name": m.name,
            "form": m.tri("form"),
            "tagline": m.tri("tagline"),
            "accuracy": m.accuracy,
            "current": m.current,
            "interfaces": m.interface_list(),
            "specs": [
                {"label": sp.tri("label"), "value": sp.value()}
                for sp in _published(m.specs.all())
            ],
            "features": [
                {"text": f.tri("text"), "image": _img(request, f.image)}
                for f in _published(m.features.all())
            ],
        })

    return {
        "categories": categories,
        "products": products,
        "technology": [
            {"icon": t.icon, "title": t.tri("title"), "text": t.tri("text")}
            for t in _published(models.MeterTechnology.objects.all())
        ],
        "docTypes": [
            d.tri("label") for d in _published(models.MeterDocType.objects.all())
        ],
    }


# ---------------------------------------------------------------------------
# news, galleries, i18n
# ---------------------------------------------------------------------------
def _news(request):
    items = []
    for n in _published(models.News.objects.all()):
        items.append({
            "date": n.date.isoformat(),
            "title": n.tri("title"),
            "body": n.tri("body"),
            "image": _img(request, n.image),
        })
    return items


def _galleries(request):
    out = {key: [] for key, _ in models.SECTION_CHOICES}
    for g in _published(models.GalleryImage.objects.all()):
        out.setdefault(g.section, []).append({
            "image": _img(request, g.image),
            "alt": g.alt,
            "caption": g.tri("caption"),
        })
    return out


def _i18n():
    bundle = {"hy": {}, "ru": {}, "en": {}}
    for s in models.UIString.objects.all():
        bundle["hy"][s.key] = s.hy
        bundle["ru"][s.key] = s.ru
        bundle["en"][s.key] = s.en
    return bundle


# ---------------------------------------------------------------------------
# top-level
# ---------------------------------------------------------------------------
def build_content(request=None):
    return {
        "company": _company(request),
        "construction": _construction(request),
        "switchgear": _switchgear(request),
        "meters": _meters(request),
        "news": _news(request),
        "galleries": _galleries(request),
        "i18n": _i18n(),
    }


# ---------------------------------------------------------------------------
# contact form intake
# ---------------------------------------------------------------------------
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]

    def validate(self, attrs):
        if not attrs.get("name"):
            raise serializers.ValidationError({"name": "Name is required."})
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError(
                "Please provide at least an email or a phone number."
            )
        return attrs
