# Generated by Django 4.2.4 on 2023-10-06 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0082_allowedip'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ip_restricted',
            field=models.BooleanField(default=False),
        ),
    ]
