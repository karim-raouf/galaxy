# Generated by Django 2.1.15 on 2023-08-17 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0006_auto_20230817_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
