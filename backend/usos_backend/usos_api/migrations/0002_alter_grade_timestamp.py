# Generated by Django 5.1.3 on 2024-12-17 13:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usos_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
