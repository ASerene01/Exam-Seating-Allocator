# Generated by Django 4.2.7 on 2024-02-09 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0032_event_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventcourses",
            name="event",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="eventcourse",
                to="api.event",
            ),
        ),
        migrations.CreateModel(
            name="EventHalls",
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
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eventhall",
                        to="api.event",
                    ),
                ),
                (
                    "hall",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event",
                        to="api.hall",
                    ),
                ),
            ],
        ),
    ]
