# Generated by Django 5.1.4 on 2025-03-14 10:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_doctor_total_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewcount',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='viewcount',
            name='user',
        ),
        migrations.AddField(
            model_name='viewcount',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
