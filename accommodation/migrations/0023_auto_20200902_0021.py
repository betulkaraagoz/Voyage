# Generated by Django 3.1 on 2020-09-01 21:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0022_auto_20200901_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 1, 21, 21, 45, 504251, tzinfo=utc)),
        ),
    ]