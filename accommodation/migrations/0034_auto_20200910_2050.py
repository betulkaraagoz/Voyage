# Generated by Django 3.1 on 2020-09-10 17:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0033_auto_20200909_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 10, 17, 50, 27, 800623, tzinfo=utc)),
        ),
    ]