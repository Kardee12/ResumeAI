# Generated by Django 5.0.3 on 2024-05-06 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_job_employer_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='position',
            field=models.CharField(default='Unknown', max_length=120),
        ),
    ]
