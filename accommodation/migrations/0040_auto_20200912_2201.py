# Generated by Django 3.1 on 2020-09-12 19:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0039_auto_20200911_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 12, 19, 1, 48, 746016, tzinfo=utc)),
        ),
    ]
