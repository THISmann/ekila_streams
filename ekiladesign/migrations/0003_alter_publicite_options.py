# Generated by Django 4.2.6 on 2023-11-18 21:55
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ekiladesign", "0002_alter_publicite_is_updated_at"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="publicite",
            options={
                "ordering": ["-is_created_at"],
                "verbose_name": "Publicite",
                "verbose_name_plural": "Publicities",
            },
        ),
    ]
