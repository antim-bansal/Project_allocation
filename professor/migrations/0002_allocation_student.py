# Generated by Django 4.2.5 on 2024-03-28 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('professor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]
