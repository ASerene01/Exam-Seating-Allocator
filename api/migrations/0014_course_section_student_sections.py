# Generated by Django 4.2.6 on 2023-10-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_alter_user_user_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Section",
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
                ("section_name", models.CharField(max_length=50)),
                (
                    "courses",
                    models.ManyToManyField(
                        related_name="courses_section", to="api.course"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="student",
            name="sections",
            field=models.ManyToManyField(related_name="students", to="api.section"),
        ),
    ]
