# Generated by Django 4.2.5 on 2023-10-24 05:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rte",
            name="admin_code",
        ),
        migrations.RemoveField(
            model_name="rte",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="student",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="teacher",
            name="date_joined",
        ),
    ]
