# Generated by Django 4.2.4 on 2023-09-18 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0069_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Gender',
            field=models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True),
        ),
    ]
