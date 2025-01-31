# Generated by Django 5.1.4 on 2025-01-18 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='medical_report',
            field=models.FileField(blank=True, help_text='Upload any previous report or prescriptions if you have. ( Maximum file size 2MB )', null=True, upload_to='medical_reports/'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]
