# Generated by Django 3.1 on 2020-08-24 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0004_hotel_location_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='room',
            name='img',
        ),
    ]
