# Generated by Django 5.1.4 on 2025-02-09 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_alter_customuser_profile_image'),
        ('doctors', '0005_remove_appointment_medical_report'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'ordering': ['appointment_date', 'appointment_time', 'created_at']},
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.CharField(blank=True, choices=[('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('02:00 PM', '02:00 PM'), ('03:00 PM', '03:00 PM'), ('04:00 PM', '04:00 PM')], max_length=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('patient', 'appointment_date', 'appointment_time')},
        ),
    ]
