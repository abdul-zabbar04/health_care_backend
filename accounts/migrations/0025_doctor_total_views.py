# Generated by Django 5.1.4 on 2025-03-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_remove_viewcount_user_viewcount_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='total_views',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
