# Generated by Django 4.2.6 on 2023-10-27 04:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_remove_rte_email_remove_rte_employee_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="use_image",
            field=models.ImageField(
                default="myapp\\Pictures\\Users\\default.jpg",
                upload_to="myapp\\Pictures\\Users",
            ),
        ),
    ]
