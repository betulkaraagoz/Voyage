# Generated by Django 3.1 on 2020-09-09 17:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0032_auto_20200909_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='address',
        ),
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 9, 17, 47, 4, 691972, tzinfo=utc)),
        ),
    ]
