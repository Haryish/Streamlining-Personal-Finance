# Generated by Django 4.2.9 on 2024-07-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Others", "Others")],
                default="Male",
                max_length=10,
            ),
        ),
    ]
