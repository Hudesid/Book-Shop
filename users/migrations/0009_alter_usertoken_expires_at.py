# Generated by Django 5.1.5 on 2025-02-08 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_usertoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 8, 12, 7, 31, 859853, tzinfo=datetime.timezone.utc)),
        ),
    ]
