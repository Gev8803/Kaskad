from django.db import migrations


def update_brand_suffix(apps, schema_editor):
    UIString = apps.get_model("content", "UIString")
    UIString.objects.filter(key="brand.suffix").update(
        hy="ՀՈԼԴԻՆԳ",
        ru="ХОЛДИНГ",
        en="HOLDING",
    )


def restore_brand_suffix(apps, schema_editor):
    UIString = apps.get_model("content", "UIString")
    UIString.objects.filter(key="brand.suffix").update(
        hy="ԳՐՈՒՊ",
        ru="ГРУПП",
        en="GROUP",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_switchgearitem_notes_en_switchgearitem_notes_hy_and_more"),
    ]

    operations = [
        migrations.RunPython(update_brand_suffix, restore_brand_suffix),
    ]
