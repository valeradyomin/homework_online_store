# Generated by Django 4.2.7 on 2023-12-20 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'verbose_name': 'версия', 'verbose_name_plural': 'версии'},
        ),
    ]
