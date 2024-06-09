# Generated by Django 4.1 on 2024-04-24 18:26

from django.db import migrations, models
import professor.models


class Migration(migrations.Migration):

    dependencies = [
        ("professor", "0009_deadline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deadline",
            name="deadline",
            field=models.DateTimeField(
                default=professor.models.Deadline.default_deadline
            ),
        ),
    ]