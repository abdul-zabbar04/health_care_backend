# Generated by Django 5.1.4 on 2025-01-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_patient_height_in_alter_patient_height_ft_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='height_in',
            field=models.IntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], null=True),
        ),
    ]
