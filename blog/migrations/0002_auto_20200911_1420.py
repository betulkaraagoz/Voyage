# Generated by Django 3.1 on 2020-09-11 11:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='video_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 11, 11, 20, 11, 602433, tzinfo=utc)),
        ),
    ]
