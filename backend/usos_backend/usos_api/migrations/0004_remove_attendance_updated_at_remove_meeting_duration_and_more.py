# Generated by Django 5.1.3 on 2024-12-17 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usos_api', '0003_attendance_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='scheduledmeeting',
            name='duration',
        ),
    ]