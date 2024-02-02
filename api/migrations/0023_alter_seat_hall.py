# Generated by Django 4.2.7 on 2024-01-19 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0022_alter_seat_hall"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seat",
            name="hall",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="seats",
                to="api.hall",
            ),
        ),
    ]