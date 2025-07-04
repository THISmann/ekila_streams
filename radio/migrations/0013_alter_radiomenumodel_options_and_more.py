# Generated by Django 4.2.6 on 2024-05-10 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("radio", "0012_alter_radiomenumodel_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="radiomenumodel",
            options={
                "verbose_name": "radio menu",
                "verbose_name_plural": "radio menus",
            },
        ),
        migrations.AlterField(
            model_name="radiomenumodel",
            name="link",
            field=models.URLField(verbose_name="link"),
        ),
        migrations.AlterField(
            model_name="radiomenumodel",
            name="radio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="radio_menu",
                to="radio.radio",
                verbose_name="radio",
            ),
        ),
        migrations.AlterField(
            model_name="radiomenumodel",
            name="title",
            field=models.CharField(max_length=255, verbose_name="title"),
        ),
    ]
