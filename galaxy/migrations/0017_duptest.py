# Generated by Django 4.2.4 on 2023-08-21 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0016_delete_hezar'),
    ]

    operations = [
        migrations.CreateModel(
            name='DupTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
    ]
