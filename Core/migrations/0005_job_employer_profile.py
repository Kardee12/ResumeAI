# Generated by Django 5.0.3 on 2024-05-05 23:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_job_applicant_count_job_job_uuid_employerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='employer_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='Core.employerprofile'),
        ),
    ]