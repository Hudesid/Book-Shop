# Generated by Django 5.1.5 on 2025-02-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_at',
            field=models.CharField(max_length=100),
        ),
    ]
