# Generated by Django 3.1 on 2020-08-30 11:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0015_auto_20200829_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 30, 11, 59, 22, 149778, tzinfo=utc)),
        ),
    ]
