# Generated by Django 4.2.7 on 2024-01-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0025_remove_seat_hall_seat_hall"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hall",
            name="noOfSeats",
            field=models.IntegerField(default=1),
        ),
    ]
