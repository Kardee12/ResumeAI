# Generated by Django 5.0.3 on 2024-05-02 20:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Core", "0002_remove_userresume_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="skills",
            field=models.TextField(blank=True, null=True),
        ),
    ]