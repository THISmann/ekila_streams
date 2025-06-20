# Generated by Django 4.2.6 on 2024-03-22 03:26
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("radio", "0004_alter_radio_url_server_radio"),
    ]

    operations = [
        migrations.CreateModel(
            name="RadioMenuModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("link", models.URLField()),
            ],
            options={
                "verbose_name": "RadioMenu",
                "verbose_name_plural": "RadioMenus",
            },
        ),
        migrations.AddIndex(
            model_name="radio",
            index=models.Index(fields=["user"], name="radio_by_user"),
        ),
        migrations.AddField(
            model_name="radiomenumodel",
            name="radio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="radio_menu",
                to="radio.radio",
            ),
        ),
    ]
