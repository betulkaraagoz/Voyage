# Generated by Django 3.1 on 2020-09-01 21:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0024_auto_20200902_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 1, 21, 59, 31, 554544, tzinfo=utc)),
        ),
    ]
