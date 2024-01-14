# Generated by Django 4.2.9 on 2024-01-14 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("health", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Treatment",
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
                ("date_of_treatment", models.DateTimeField(auto_now_add=True)),
                ("treatment_method", models.TextField(max_length=300)),
                ("notes", models.TextField(null=True)),
                (
                    "treatment_status",
                    models.CharField(
                        choices=[
                            ("Scheduled", "Scheduled"),
                            ("In Progress", "In Progress"),
                            ("Completed", "Completed"),
                            ("Cancelled", "Cancelled"),
                            ("Postponed", "Postponed"),
                        ],
                        default="Scheduled",
                        max_length=15,
                    ),
                ),
                ("completion_date", models.DateTimeField(null=True)),
                (
                    "cow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.cow"
                    ),
                ),
                (
                    "disease",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="health.disease"
                    ),
                ),
            ],
        ),
    ]
