# Generated by Django 3.1 on 2020-08-30 17:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0018_auto_20200830_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 30, 17, 7, 17, 568281, tzinfo=utc)),
        ),
    ]
