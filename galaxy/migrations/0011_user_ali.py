# Generated by Django 2.1.15 on 2023-08-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0010_auto_20230817_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ali',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]
