"""
Admin CMS configuration.

The Django admin IS the content-management panel: secure login, protected
routes, CRUD, search, filtering and pagination come built in. Everything below
tailors it to Kaskad's content — image thumbnails, inline editors for child
rows, inline publish/sort editing, language-grouped fieldsets and a logical,
sectioned index.
"""
from django.contrib import admin
from django.utils.html import format_html

from . import models


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def thumb(obj, field="image", h=46):
    f = getattr(obj, field, None)
    if not f:
        return format_html('<span style="color:#999">—</span>')
    try:
        url = f.url
    except ValueError:
        return format_html('<span style="color:#999">—</span>')
    return format_html(
        '<img src="{}" style="height:{}px;width:auto;border-radius:6px;'
        'object-fit:cover;box-shadow:0 1px 3px rgba(0,0,0,.25)" />',
        url, h,
    )


class PublishedListMixin:
    """Common list controls: inline publish/sort editing + a published filter."""

    list_per_page = 25

    def get_list_display(self, request):
        base = list(super().get_list_display(request))
        for extra in ("sort", "is_published"):
            if extra not in base:
                base.append(extra)
        return base

    def get_list_editable(self, request):
        return ("sort", "is_published")

    def changelist_view(self, request, extra_context=None):
        # Attach list_editable dynamically so subclasses need not repeat it.
        self.list_editable = self.get_list_editable(request)
        return super().changelist_view(request, extra_context)


# ---------------------------------------------------------------------------
# Company / global
# ---------------------------------------------------------------------------
@admin.register(models.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact", {"fields": ("phone", "phone_link", "email", "map_embed")}),
        ("Address", {"fields": ("address_hy", "address_ru", "address_en")}),
        ("Switchgear — manufacturing text", {
            "fields": ("manufacturing_hy", "manufacturing_ru", "manufacturing_en"),
        }),
    )

    def has_add_permission(self, request):
        # Singleton: never more than one row.
        return not models.SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Stat)
class StatAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__", "value", "suffix", "label_ru")
    search_fields = ("label_hy", "label_ru", "label_en")
    fieldsets = (
        (None, {"fields": ("value", "suffix", ("sort", "is_published"))}),
        ("Label", {"fields": ("label_hy", "label_ru", "label_en")}),
    )


class IconTitleTextAdmin(PublishedListMixin, admin.ModelAdmin):
    """Shared admin for Advantage / Value / MeterTechnology."""
    list_display = ("__str__", "icon")
    search_fields = ("title_hy", "title_ru", "title_en", "text_hy", "text_ru", "text_en")
    fieldsets = (
        (None, {"fields": ("icon", ("sort", "is_published"))}),
        ("Title", {"fields": ("title_hy", "title_ru", "title_en")}),
        ("Text", {"fields": ("text_hy", "text_ru", "text_en")}),
    )


@admin.register(models.Advantage)
class AdvantageAdmin(IconTitleTextAdmin):
    pass


@admin.register(models.Value)
class ValueAdmin(IconTitleTextAdmin):
    pass


@admin.register(models.Partner)
class PartnerAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("name", "logo_preview")
    search_fields = ("name",)
    readonly_fields = ("logo_preview",)
    fields = ("name", "logo", "logo_preview", ("sort", "is_published"))

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        return thumb(obj, "logo")


@admin.register(models.Client)
class ClientAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__", "logo_preview")
    search_fields = ("name_hy", "name_ru", "name_en")
    readonly_fields = ("logo_preview",)
    fieldsets = (
        (None, {"fields": ("logo", "logo_preview", ("sort", "is_published"))}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        return thumb(obj, "logo")


@admin.register(models.HistoryMilestone)
class HistoryMilestoneAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("year", "text_ru")
    search_fields = ("year", "text_hy", "text_ru", "text_en")
    fieldsets = (
        (None, {"fields": ("year", ("sort", "is_published"))}),
        ("Text", {"fields": ("text_hy", "text_ru", "text_en")}),
    )


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class ServicePointInline(admin.TabularInline):
    model = models.ServicePoint
    extra = 1
    fields = ("text_ru", "text_hy", "text_en", "sort", "is_published")


@admin.register(models.Service)
class ServiceAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__", "slug", "icon")
    search_fields = ("slug", "name_hy", "name_ru", "name_en")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [ServicePointInline]
    fieldsets = (
        (None, {"fields": ("slug", "icon", ("sort", "is_published"))}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
        ("Summary", {"fields": ("summary_hy", "summary_ru", "summary_en")}),
    )


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__", "slug")
    search_fields = ("slug", "name_hy", "name_ru", "name_en")
    fieldsets = (
        (None, {"fields": ("slug", ("sort", "is_published"))}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
    )


class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    extra = 1
    fields = ("image", "preview", "alt", "sort", "is_published")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return thumb(obj)


@admin.register(models.Project)
class ProjectAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "__str__", "category", "year", "country")
    list_display_links = ("cover", "__str__")
    list_filter = ("category", "country", "is_published")
    search_fields = ("slug", "name_hy", "name_ru", "name_en", "client_ru", "spec")
    prepopulated_fields = {"slug": ("name_en",)}
    readonly_fields = ("cover",)
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {"fields": (
            "slug", "image", "cover", "category", "country", "year", "spec",
            ("sort", "is_published"),
        )}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
        ("Location", {"fields": ("location_hy", "location_ru", "location_en")}),
        ("Client", {"fields": ("client_hy", "client_ru", "client_en")}),
        ("Description", {"fields": ("description_hy", "description_ru", "description_en")}),
    )

    @admin.display(description="Cover")
    def cover(self, obj):
        return thumb(obj)


# ---------------------------------------------------------------------------
# Switchgear
# ---------------------------------------------------------------------------
class SwitchgearItemInline(admin.TabularInline):
    model = models.SwitchgearItem
    extra = 0
    fields = ("code", "image", "preview", "name_ru", "sort", "is_published")
    readonly_fields = ("preview",)
    show_change_link = True  # open the module's own full detail page

    @admin.display(description="Cover")
    def preview(self, obj):
        return thumb(obj)


class SwitchgearItemImageInline(admin.TabularInline):
    model = models.SwitchgearItemImage
    extra = 1
    fields = ("image", "preview", "alt", "sort", "is_published")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return thumb(obj)


class SwitchgearItemBulletInline(admin.TabularInline):
    model = models.SwitchgearItemBullet
    extra = 1
    fields = ("kind", "text_ru", "text_hy", "text_en", "sort", "is_published")


class SwitchgearItemSpecRowInline(admin.TabularInline):
    model = models.SwitchgearItemSpecRow
    extra = 1
    fields = ("param_ru", "param_hy", "param_en", "unit", "v1", "v2", "v3", "is_group", "sort")


@admin.register(models.SwitchgearItem)
class SwitchgearItemAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "code", "category", "__str__")
    list_display_links = ("cover", "code")
    list_filter = ("category", "is_published")
    search_fields = ("code", "name_hy", "name_ru", "name_en")
    readonly_fields = ("cover",)
    inlines = [SwitchgearItemImageInline, SwitchgearItemSpecRowInline, SwitchgearItemBulletInline]
    fieldsets = (
        (None, {"fields": ("category", "code", "image", "cover", "pdf", ("sort", "is_published"))}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
        ("Description", {"fields": ("description_hy", "description_ru", "description_en")}),
        ("Purpose", {"fields": ("purpose_hy", "purpose_ru", "purpose_en")}),
        ("Spec table", {"fields": ("spec_cols", "notes_hy", "notes_ru", "notes_en")}),
        ("Fuse table (advanced)", {"classes": ("collapse",), "fields": ("fuse_table",)}),
    )

    @admin.display(description="Cover")
    def cover(self, obj):
        return thumb(obj)


class SwitchgearSpecInline(admin.TabularInline):
    model = models.SwitchgearSpec
    extra = 1
    fields = ("label_ru", "value_plain", "value_ru", "sort", "is_published")


class SwitchgearDocInline(admin.TabularInline):
    model = models.SwitchgearDoc
    extra = 1
    fields = ("label_ru", "file", "href", "sort", "is_published")


@admin.register(models.SwitchgearCategory)
class SwitchgearCategoryAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "__str__", "slug", "voltage")
    list_display_links = ("cover", "__str__")
    search_fields = ("slug", "name_hy", "name_ru", "name_en", "voltage")
    prepopulated_fields = {"slug": ("name_en",)}
    readonly_fields = ("cover",)
    inlines = [SwitchgearItemInline, SwitchgearSpecInline, SwitchgearDocInline]
    fieldsets = (
        (None, {"fields": ("slug", "image", "cover", "voltage", ("sort", "is_published"))}),
        ("Current rating", {"fields": ("current_hy", "current_ru", "current_en")}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
        ("Summary", {"fields": ("summary_hy", "summary_ru", "summary_en")}),
        ("Description", {"fields": ("description_hy", "description_ru", "description_en")}),
    )

    @admin.display(description="Cover")
    def cover(self, obj):
        return thumb(obj)


@admin.register(models.Certificate)
class CertificateAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "__str__")
    list_display_links = ("cover", "__str__")
    search_fields = ("title_hy", "title_ru", "title_en")
    readonly_fields = ("cover",)
    fieldsets = (
        (None, {"fields": ("image", "cover", ("sort", "is_published"))}),
        ("Title", {"fields": ("title_hy", "title_ru", "title_en")}),
    )

    @admin.display(description="Image")
    def cover(self, obj):
        return thumb(obj)


# ---------------------------------------------------------------------------
# Meters
# ---------------------------------------------------------------------------
@admin.register(models.MeterCategory)
class MeterCategoryAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__", "slug")
    search_fields = ("slug", "name_hy", "name_ru", "name_en")
    fieldsets = (
        (None, {"fields": ("slug", ("sort", "is_published"))}),
        ("Name", {"fields": ("name_hy", "name_ru", "name_en")}),
    )


class MeterSpecInline(admin.TabularInline):
    model = models.MeterSpec
    extra = 1
    fields = ("label_ru", "value_plain", "value_ru", "sort", "is_published")


class MeterFeatureInline(admin.TabularInline):
    model = models.MeterFeature
    extra = 1
    fields = ("image", "preview", "text_ru", "text_hy", "text_en", "sort", "is_published")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        return thumb(obj)


@admin.register(models.Meter)
class MeterAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "name", "category", "accuracy", "current")
    list_display_links = ("cover", "name")
    list_filter = ("category", "is_published")
    search_fields = ("name", "slug", "tagline_ru", "tagline_en", "accuracy")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("cover",)
    inlines = [MeterSpecInline, MeterFeatureInline]
    fieldsets = (
        (None, {"fields": (
            "name", "slug", "category", "image", "cover",
            "accuracy", "current", "interfaces", ("sort", "is_published"),
        )}),
        ("Form factor", {"fields": ("form_hy", "form_ru", "form_en")}),
        ("Tagline", {"fields": ("tagline_hy", "tagline_ru", "tagline_en")}),
    )

    @admin.display(description="Photo")
    def cover(self, obj):
        return thumb(obj)


@admin.register(models.MeterTechnology)
class MeterTechnologyAdmin(IconTitleTextAdmin):
    pass


@admin.register(models.MeterDocType)
class MeterDocTypeAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("__str__",)
    search_fields = ("label_hy", "label_ru", "label_en")
    fieldsets = (
        (None, {"fields": (("sort", "is_published"),)}),
        ("Label", {"fields": ("label_hy", "label_ru", "label_en")}),
    )


# ---------------------------------------------------------------------------
# News & galleries
# ---------------------------------------------------------------------------
@admin.register(models.News)
class NewsAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "__str__", "date")
    list_display_links = ("cover", "__str__")
    list_filter = ("is_published", "date")
    search_fields = ("slug", "title_hy", "title_ru", "title_en")
    date_hierarchy = "date"
    prepopulated_fields = {"slug": ("title_en",)}
    readonly_fields = ("cover",)
    fieldsets = (
        (None, {"fields": ("slug", "date", "image", "cover", ("sort", "is_published"))}),
        ("Title", {"fields": ("title_hy", "title_ru", "title_en")}),
        ("Body", {"fields": ("body_hy", "body_ru", "body_en")}),
    )

    def get_list_editable(self, request):
        return ("is_published",)  # date-ordered; sort is secondary

    @admin.display(description="Image")
    def cover(self, obj):
        return thumb(obj)


@admin.register(models.GalleryImage)
class GalleryImageAdmin(PublishedListMixin, admin.ModelAdmin):
    list_display = ("cover", "section", "alt", "caption_ru")
    list_display_links = ("cover",)
    list_filter = ("section", "is_published")
    search_fields = ("alt", "caption_hy", "caption_ru", "caption_en")
    readonly_fields = ("cover",)
    fieldsets = (
        (None, {"fields": ("section", "image", "cover", "alt", ("sort", "is_published"))}),
        ("Caption", {"fields": ("caption_hy", "caption_ru", "caption_en")}),
    )

    @admin.display(description="Image")
    def cover(self, obj):
        return thumb(obj)


# ---------------------------------------------------------------------------
# UI strings & contact messages
# ---------------------------------------------------------------------------
@admin.register(models.UIString)
class UIStringAdmin(admin.ModelAdmin):
    list_display = ("key", "ru", "en")
    search_fields = ("key", "hy", "ru", "en")
    list_per_page = 50


@admin.register(models.ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at", "is_handled")
    list_filter = ("is_handled", "created_at")
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False  # messages only arrive via the public form
