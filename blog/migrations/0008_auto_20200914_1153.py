# Generated by Django 3.1 on 2020-09-14 08:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200912_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 14, 8, 53, 17, 789904, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='subtitle',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='video_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
