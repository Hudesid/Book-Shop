# Generated by Django 5.1.5 on 2025-02-08 08:42

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_usertoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 8, 8, 46, 4, 148632, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
