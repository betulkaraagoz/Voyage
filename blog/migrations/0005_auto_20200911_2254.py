# Generated by Django 3.1 on 2020-09-11 19:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200911_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 11, 19, 54, 36, 285738, tzinfo=utc)),
        ),
    ]
