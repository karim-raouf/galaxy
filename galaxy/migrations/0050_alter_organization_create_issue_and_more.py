# Generated by Django 4.2.4 on 2023-09-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0049_alter_organization_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='Create_Issue',
            field=models.BooleanField(verbose_name='Automaticlly create inter-store issue inventory orders :'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='Create_Receive',
            field=models.BooleanField(verbose_name='Automaticlly create inter-store receive inventory orders :'),
        ),
    ]
