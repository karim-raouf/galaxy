# Generated by Django 2.1.15 on 2023-08-17 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0009_user_kk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='kk',
        ),
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='user',
            name='usee',
        ),
    ]
