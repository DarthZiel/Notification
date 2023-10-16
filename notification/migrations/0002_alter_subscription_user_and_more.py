# Generated by Django 4.2.6 on 2023-10-16 01:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notification", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="user",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name="subscription",
            unique_together={("user", "author")},
        ),
    ]
