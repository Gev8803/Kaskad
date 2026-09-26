"""
Automatic image optimisation.

When an image is uploaded through the admin, `optimize_image()` downscales it to
a sensible maximum width and re-encodes it (JPEG quality 82 / PNG optimize) so
the frontend loads fast without any manual work by the editor. Aspect ratio is
always preserved and images are never upscaled.
"""
from io import BytesIO

from django.core.files.base import ContentFile

try:
    from PIL import Image, ImageOps
    _PIL_OK = True
except Exception:  # pragma: no cover
    _PIL_OK = False

MAX_WIDTH = 1600          # px; wide enough for full-bleed hero/gallery use
JPEG_QUALITY = 82


def optimize_image(field_file, max_width=MAX_WIDTH):
    """Optimise an ImageField's file in place. Safe to call unconditionally.

    Returns True if the file was rewritten, False otherwise.
    """
    if not _PIL_OK or not field_file:
        return False

    name = field_file.name
    storage = field_file.storage

    # Read the whole file into memory and close it FIRST. On Windows the file
    # cannot be deleted/overwritten while the FieldFile handle is still open.
    try:
        field_file.open("rb")
        raw = field_file.read()
    except Exception:
        return False
    finally:
        try:
            field_file.close()
        except Exception:
            pass

    try:
        img = Image.open(BytesIO(raw))
        img_format = (img.format or "").upper()
        img.load()
    except Exception:
        return False

    # Respect EXIF orientation, then drop the metadata.
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    lower = name.lower()
    is_jpeg = img_format in ("JPEG", "JPG") or lower.endswith((".jpg", ".jpeg"))
    is_png = img_format == "PNG" or lower.endswith(".png")
    is_webp = img_format == "WEBP" or lower.endswith(".webp")
    if not (is_jpeg or is_png or is_webp):
        # Unknown/animated format (e.g. GIF, SVG): leave untouched.
        return False

    # Downscale if wider than the cap.
    if img.width > max_width:
        ratio = max_width / float(img.width)
        img = img.resize((max_width, max(1, int(img.height * ratio))), Image.LANCZOS)

    buffer = BytesIO()
    if is_jpeg:
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        img.save(buffer, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    elif is_png:
        img.save(buffer, format="PNG", optimize=True)
    else:  # webp
        img.save(buffer, format="WEBP", quality=JPEG_QUALITY, method=6)

    optimized = buffer.getvalue()
    # Only rewrite if we actually made it smaller (avoids growing tiny images).
    if len(optimized) >= len(raw):
        return False

    try:
        if storage.exists(name):
            storage.delete(name)
        storage.save(name, ContentFile(optimized))
    except Exception:
        return False
    return True
