# Generated by Django 3.1 on 2020-09-01 21:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0023_auto_20200902_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 1, 21, 51, 15, 317977, tzinfo=utc)),
        ),
    ]
