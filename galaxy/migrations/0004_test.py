# Generated by Django 2.1.15 on 2023-08-16 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0003_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
