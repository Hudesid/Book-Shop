# Generated by Django 5.1.5 on 2025-02-07 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_created_at_user_date_joined_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 7, 18, 39, 57, 380763, tzinfo=datetime.timezone.utc)),
        ),
    ]
