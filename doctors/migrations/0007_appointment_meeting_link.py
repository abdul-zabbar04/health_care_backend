# Generated by Django 5.1.4 on 2025-02-09 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0006_alter_appointment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='meeting_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
