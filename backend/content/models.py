"""
Data models for the Kaskad Group CMS.

Design notes
------------
* Trilingual text uses three sibling columns per field: ``<field>_hy`` /
  ``<field>_ru`` / ``<field>_en``. This keeps all three languages on one admin
  form and serialises directly to the ``{hy, ru, en}`` objects the existing
  frontend (``site/assets/js/app.js``) already expects.
* ``TriMixin.tri("name")`` builds that dict from ``name_hy/name_ru/name_en``.
* Every publicly displayed model inherits ``Orderable`` (``sort`` +
  ``is_published``); the API returns only published rows, ordered by ``sort``.
* ``ImageOptimizedModel`` runs Pillow optimisation on save for its image fields.
"""
from django.db import models

from .imaging import optimize_image

# Icon names available to app.js (see the ICONS set in site/assets/js/app.js)
ICON_CHOICES = [
    ("bolt", "bolt"), ("factory", "factory"), ("blueprint", "blueprint"),
    ("network", "network"), ("gauge", "gauge"), ("test", "test"),
    ("cycle", "cycle"), ("medal", "medal"), ("globe", "globe"),
    ("team", "team"), ("shield", "shield"), ("wifi", "wifi"),
    ("code", "code"), ("clock", "clock"), ("bulb", "bulb"),
    ("leaf", "leaf"), ("box", "box"),
]

SECTION_CHOICES = [
    ("construction", "Construction"),
    ("switchgear", "Switchgear"),
    ("meters", "Meters"),
]


# ---------------------------------------------------------------------------
# Mixins / abstract bases
# ---------------------------------------------------------------------------
class TriMixin:
    """Adds a helper to assemble a {hy, ru, en} dict from sibling columns."""

    def tri(self, base):
        return {
            "hy": getattr(self, f"{base}_hy", "") or "",
            "ru": getattr(self, f"{base}_ru", "") or "",
            "en": getattr(self, f"{base}_en", "") or "",
        }


class Orderable(models.Model):
    sort = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )
    is_published = models.BooleanField(
        default=True, help_text="Untick to hide this item from the website (draft)."
    )

    class Meta:
        abstract = True
        ordering = ["sort", "id"]


class ImageOptimizedModel(models.Model):
    """Base model that optimises its image fields on save."""

    OPTIMIZE_FIELDS = []  # names of ImageField attributes to optimise

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        dirty = False
        for field_name in self.OPTIMIZE_FIELDS:
            f = getattr(self, field_name, None)
            if f and hasattr(f, "path"):
                try:
                    if optimize_image(f):
                        dirty = True
                except Exception:
                    pass
        if dirty:
            super().save(update_fields=self.OPTIMIZE_FIELDS)


def tri_field(verbose, **kwargs):
    """Factory for an optional trilingual text column."""
    return models.TextField(verbose, blank=True, **kwargs)


def tri_char(verbose, max_length=255, **kwargs):
    return models.CharField(verbose, max_length=max_length, blank=True, **kwargs)


# ---------------------------------------------------------------------------
# Company / global
# ---------------------------------------------------------------------------
class SiteSettings(TriMixin, models.Model):
    """Single-row model holding company-wide contact + narrative content."""

    address_hy = tri_char("Address (HY)")
    address_ru = tri_char("Address (RU)")
    address_en = tri_char("Address (EN)")
    phone = models.CharField(max_length=64, blank=True)
    phone_link = models.CharField(
        max_length=64, blank=True, help_text="Digits only, e.g. +37477241212"
    )
    email = models.EmailField(blank=True)
    map_embed = models.URLField(
        max_length=600, blank=True, help_text="Google Maps embed URL"
    )
    # Switchgear manufacturing narrative (DATA.switchgear.manufacturing)
    manufacturing_hy = tri_field("Manufacturing text (HY)")
    manufacturing_ru = tri_field("Manufacturing text (RU)")
    manufacturing_en = tri_field("Manufacturing text (EN)")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Stat(TriMixin, Orderable):
    value = models.IntegerField()
    suffix = models.CharField(max_length=8, blank=True, help_text='e.g. "+"')
    label_hy = tri_char("Label (HY)")
    label_ru = tri_char("Label (RU)")
    label_en = tri_char("Label (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Statistic"

    def __str__(self):
        return f"{self.value}{self.suffix} — {self.label_en or self.label_ru}"


class Advantage(TriMixin, Orderable):
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="medal")
    title_hy = tri_char("Title (HY)")
    title_ru = tri_char("Title (RU)")
    title_en = tri_char("Title (EN)")
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Advantage"

    def __str__(self):
        return self.title_en or self.title_ru or f"Advantage #{self.pk}"


class Value(TriMixin, Orderable):
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="bulb")
    title_hy = tri_char("Title (HY)")
    title_ru = tri_char("Title (RU)")
    title_en = tri_char("Title (EN)")
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Company value"

    def __str__(self):
        return self.title_en or self.title_ru or f"Value #{self.pk}"


class Partner(ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["logo"]
    name = models.CharField(max_length=160)
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)

    class Meta(Orderable.Meta):
        verbose_name = "Partner"

    def __str__(self):
        return self.name


class Client(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["logo"]
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)

    class Meta(Orderable.Meta):
        verbose_name = "Client"

    def __str__(self):
        return self.name_en or self.name_ru or f"Client #{self.pk}"


class HistoryMilestone(TriMixin, Orderable):
    year = models.CharField(max_length=32)
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "History milestone"

    def __str__(self):
        return f"{self.year}"


# ---------------------------------------------------------------------------
# Construction division
# ---------------------------------------------------------------------------
class Service(TriMixin, Orderable):
    slug = models.SlugField(max_length=80, unique=True)
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="bolt")
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")
    summary_hy = tri_field("Summary (HY)")
    summary_ru = tri_field("Summary (RU)")
    summary_en = tri_field("Summary (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Service"

    def __str__(self):
        return self.name_en or self.name_ru or self.slug


class ServicePoint(TriMixin, Orderable):
    service = models.ForeignKey(
        Service, related_name="points", on_delete=models.CASCADE
    )
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Service point"

    def __str__(self):
        return self.text_en or self.text_ru or f"Point #{self.pk}"


class ProjectCategory(TriMixin, Orderable):
    slug = models.SlugField(max_length=60, unique=True)
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Project category"
        verbose_name_plural = "Project categories"

    def __str__(self):
        return self.name_en or self.name_ru or self.slug


class Project(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    slug = models.SlugField(max_length=80, unique=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    country = models.CharField(
        max_length=8, blank=True, help_text='ISO-ish code, e.g. "am", "ru"'
    )
    year = models.CharField(max_length=32, blank=True)
    # Non-FK category slug matches project filter chips (substation/generation/...)
    category = models.CharField(max_length=60, blank=True)
    spec = models.CharField(
        max_length=120, blank=True, help_text='e.g. "220 kV · 125 MVA"'
    )
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")
    location_hy = tri_char("Location (HY)")
    location_ru = tri_char("Location (RU)")
    location_en = tri_char("Location (EN)")
    client_hy = tri_char("Client (HY)")
    client_ru = tri_char("Client (RU)")
    client_en = tri_char("Client (EN)")
    description_hy = tri_field("Description (HY)")
    description_ru = tri_field("Description (RU)")
    description_en = tri_field("Description (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Project"

    def __str__(self):
        return self.name_en or self.name_ru or self.slug


class ProjectImage(ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    project = models.ForeignKey(
        Project, related_name="gallery", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="projects/gallery/")
    alt = models.CharField(max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "Project image"

    def __str__(self):
        return f"Image for {self.project_id}"


# ---------------------------------------------------------------------------
# Switchgear division
# ---------------------------------------------------------------------------
class SwitchgearCategory(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    slug = models.SlugField(max_length=80, unique=True)
    image = models.ImageField(upload_to="switchgear/", blank=True, null=True)
    voltage = models.CharField(max_length=60, blank=True)
    current_hy = tri_char("Current (HY)")
    current_ru = tri_char("Current (RU)")
    current_en = tri_char("Current (EN)")
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")
    summary_hy = tri_field("Summary (HY)")
    summary_ru = tri_field("Summary (RU)")
    summary_en = tri_field("Summary (EN)")
    description_hy = tri_field("Description (HY)")
    description_ru = tri_field("Description (RU)")
    description_en = tri_field("Description (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear category"
        verbose_name_plural = "Switchgear categories"

    def __str__(self):
        return self.name_en or self.name_ru or self.slug

    def current_is_set(self):
        return any([self.current_hy, self.current_ru, self.current_en])


class SwitchgearItem(TriMixin, ImageOptimizedModel, Orderable):
    """A full KD-2 style module/cell: cover + gallery, description, purpose,
    per-module spec table, equipment/options bullet lists, an optional fuse
    selection matrix and a downloadable PDF."""
    OPTIMIZE_FIELDS = ["image"]
    category = models.ForeignKey(
        SwitchgearCategory, related_name="items", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=60)
    image = models.ImageField(
        "Cover image", upload_to="switchgear/items/", blank=True, null=True
    )
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")
    description_hy = tri_field("Description (HY)")
    description_ru = tri_field("Description (RU)")
    description_en = tri_field("Description (EN)")
    purpose_hy = tri_field("Purpose (HY)")
    purpose_ru = tri_field("Purpose (RU)")
    purpose_en = tri_field("Purpose (EN)")
    # Header for the up-to-three spec value columns, e.g. "12 · 17.5 · 24"
    spec_cols = models.CharField(
        max_length=120, blank=True,
        help_text="Voltage column headers, separated by ·  e.g. 12 · 17.5 · 24",
    )
    notes_hy = tri_field("Spec footnotes (HY)")
    notes_ru = tri_field("Spec footnotes (RU)")
    notes_en = tri_field("Spec footnotes (EN)")
    # Optional fuse-selection matrix as JSON: {"head":"кВА/кВ","cols":[...],"rows":[[...]]}
    fuse_table = models.TextField(
        blank=True, help_text="Optional fuse-selection matrix as JSON.",
    )
    pdf = models.FileField(
        "Instruction PDF", upload_to="switchgear/docs/", blank=True, null=True
    )

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear item (cell/module)"

    def __str__(self):
        return self.code

    def spec_columns(self):
        return [c.strip() for c in self.spec_cols.split("·") if c.strip()]

    def fuse(self):
        if not self.fuse_table.strip():
            return None
        try:
            import json
            return json.loads(self.fuse_table)
        except Exception:
            return None


class SwitchgearItemImage(ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    item = models.ForeignKey(
        SwitchgearItem, related_name="gallery", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="switchgear/items/gallery/")
    alt = models.CharField(max_length=200, blank=True)

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear item image"

    def __str__(self):
        return f"Image for {self.item_id}"


class SwitchgearItemBullet(TriMixin, Orderable):
    KIND_CHOICES = [
        ("equipment", "Standard equipment"),
        ("option", "Option"),
        ("vacuum", "Vacuum-breaker option"),
    ]
    item = models.ForeignKey(
        SwitchgearItem, related_name="bullets", on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=16, choices=KIND_CHOICES, default="equipment")
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear item bullet"

    def __str__(self):
        return f"{self.kind}: {self.text_en or self.text_ru}"[:60]


class SwitchgearItemSpecRow(TriMixin, Orderable):
    item = models.ForeignKey(
        SwitchgearItem, related_name="spec_rows", on_delete=models.CASCADE
    )
    param_hy = tri_char("Parameter (HY)")
    param_ru = tri_char("Parameter (RU)")
    param_en = tri_char("Parameter (EN)")
    unit = models.CharField(max_length=40, blank=True)
    v1 = models.CharField("Value 1", max_length=60, blank=True)
    v2 = models.CharField("Value 2", max_length=60, blank=True)
    v3 = models.CharField("Value 3", max_length=60, blank=True)
    is_group = models.BooleanField(
        default=False, help_text="Render as a sub-heading row (e.g. “Module dimensions”)."
    )

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear item spec row"

    def __str__(self):
        return self.param_en or self.param_ru or f"Spec #{self.pk}"


class SwitchgearSpec(TriMixin, Orderable):
    category = models.ForeignKey(
        SwitchgearCategory, related_name="specs", on_delete=models.CASCADE
    )
    label_hy = tri_char("Label (HY)")
    label_ru = tri_char("Label (RU)")
    label_en = tri_char("Label (EN)")
    # A spec value may be a plain string (e.g. "6 / 10 / 24 kV") OR trilingual
    # (e.g. "up to 1250 A"). If any *_lang value is set, it is treated as
    # trilingual; otherwise `value_plain` is used for all languages.
    value_plain = models.CharField(max_length=200, blank=True)
    value_hy = tri_char("Value (HY)")
    value_ru = tri_char("Value (RU)")
    value_en = tri_char("Value (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear spec row"

    def __str__(self):
        return self.label_en or self.label_ru or f"Spec #{self.pk}"

    def value(self):
        if any([self.value_hy, self.value_ru, self.value_en]):
            return self.tri("value")
        return self.value_plain


class SwitchgearDoc(TriMixin, Orderable):
    category = models.ForeignKey(
        SwitchgearCategory, related_name="docs", on_delete=models.CASCADE
    )
    label_hy = tri_char("Label (HY)")
    label_ru = tri_char("Label (RU)")
    label_en = tri_char("Label (EN)")
    file = models.FileField(upload_to="switchgear/docs/", blank=True, null=True)
    href = models.CharField(
        max_length=400, blank=True, help_text="External URL (used if no file uploaded)."
    )

    class Meta(Orderable.Meta):
        verbose_name = "Switchgear document"

    def __str__(self):
        return self.label_en or self.label_ru or f"Doc #{self.pk}"


class Certificate(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    title_hy = tri_char("Title (HY)")
    title_ru = tri_char("Title (RU)")
    title_en = tri_char("Title (EN)")
    image = models.ImageField(upload_to="certs/", blank=True, null=True)

    class Meta(Orderable.Meta):
        verbose_name = "Certificate"

    def __str__(self):
        return self.title_en or self.title_ru or f"Certificate #{self.pk}"


# ---------------------------------------------------------------------------
# Meters division
# ---------------------------------------------------------------------------
class MeterCategory(TriMixin, Orderable):
    slug = models.SlugField(max_length=60, unique=True)
    name_hy = tri_char("Name (HY)")
    name_ru = tri_char("Name (RU)")
    name_en = tri_char("Name (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Meter category"
        verbose_name_plural = "Meter categories"

    def __str__(self):
        return self.name_en or self.name_ru or self.slug


class Meter(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    slug = models.SlugField(max_length=80, unique=True)
    category = models.ForeignKey(
        MeterCategory, related_name="products", on_delete=models.PROTECT
    )
    image = models.ImageField(upload_to="meters/", blank=True, null=True)
    name = models.CharField(max_length=120, help_text="Model name, e.g. МИРТЕК-12-РУ-D17")
    form_hy = tri_char("Form factor (HY)")
    form_ru = tri_char("Form factor (RU)")
    form_en = tri_char("Form factor (EN)")
    tagline_hy = tri_field("Tagline (HY)")
    tagline_ru = tri_field("Tagline (RU)")
    tagline_en = tri_field("Tagline (EN)")
    accuracy = models.CharField(max_length=60, blank=True)
    current = models.CharField(max_length=80, blank=True)
    interfaces = models.TextField(
        blank=True, help_text="One interface per line (e.g. Optical, RS-485, GSM)."
    )

    class Meta(Orderable.Meta):
        verbose_name = "Meter"

    def __str__(self):
        return self.name

    def interface_list(self):
        return [line.strip() for line in self.interfaces.splitlines() if line.strip()]


class MeterSpec(TriMixin, Orderable):
    meter = models.ForeignKey(Meter, related_name="specs", on_delete=models.CASCADE)
    label_hy = tri_char("Label (HY)")
    label_ru = tri_char("Label (RU)")
    label_en = tri_char("Label (EN)")
    value_plain = models.CharField(max_length=200, blank=True)
    value_hy = tri_char("Value (HY)")
    value_ru = tri_char("Value (RU)")
    value_en = tri_char("Value (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Meter spec row"

    def __str__(self):
        return self.label_en or self.label_ru or f"Spec #{self.pk}"

    def value(self):
        if any([self.value_hy, self.value_ru, self.value_en]):
            return self.tri("value")
        return self.value_plain


class MeterFeature(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    meter = models.ForeignKey(Meter, related_name="features", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="meters/features/", blank=True, null=True)
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Meter feature"

    def __str__(self):
        return self.text_en or self.text_ru or f"Feature #{self.pk}"


class MeterTechnology(TriMixin, Orderable):
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="wifi")
    title_hy = tri_char("Title (HY)")
    title_ru = tri_char("Title (RU)")
    title_en = tri_char("Title (EN)")
    text_hy = tri_field("Text (HY)")
    text_ru = tri_field("Text (RU)")
    text_en = tri_field("Text (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Meter technology"
        verbose_name_plural = "Meter technologies"

    def __str__(self):
        return self.title_en or self.title_ru or f"Technology #{self.pk}"


class MeterDocType(TriMixin, Orderable):
    label_hy = tri_char("Label (HY)")
    label_ru = tri_char("Label (RU)")
    label_en = tri_char("Label (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Meter document type"

    def __str__(self):
        return self.label_en or self.label_ru or f"Doc type #{self.pk}"


# ---------------------------------------------------------------------------
# News
# ---------------------------------------------------------------------------
class News(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    slug = models.SlugField(max_length=120, unique=True)
    date = models.DateField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    title_hy = tri_char("Title (HY)", max_length=300)
    title_ru = tri_char("Title (RU)", max_length=300)
    title_en = tri_char("Title (EN)", max_length=300)
    body_hy = tri_field("Body (HY)")
    body_ru = tri_field("Body (RU)")
    body_en = tri_field("Body (EN)")

    class Meta:
        ordering = ["-date", "sort"]
        verbose_name = "News item"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title_en or self.title_ru or self.slug


# ---------------------------------------------------------------------------
# Galleries (feed the three gallery sections; multi-image upload)
# ---------------------------------------------------------------------------
class GalleryImage(TriMixin, ImageOptimizedModel, Orderable):
    OPTIMIZE_FIELDS = ["image"]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True)
    caption_hy = tri_char("Caption (HY)")
    caption_ru = tri_char("Caption (RU)")
    caption_en = tri_char("Caption (EN)")

    class Meta(Orderable.Meta):
        verbose_name = "Gallery image"

    def __str__(self):
        return f"{self.section}: {self.caption_en or self.alt or self.pk}"


# ---------------------------------------------------------------------------
# UI strings (window.I18N) & contact messages
# ---------------------------------------------------------------------------
class UIString(models.Model):
    key = models.CharField(max_length=120, unique=True)
    hy = models.TextField(blank=True)
    ru = models.TextField(blank=True)
    en = models.TextField(blank=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "UI string / label"

    def __str__(self):
        return self.key


class ContactMessage(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=64, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d %H:%M}"
