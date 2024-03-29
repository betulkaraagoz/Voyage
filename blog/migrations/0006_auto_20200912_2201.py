# Generated by Django 3.1 on 2020-09-12 19:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200911_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='place',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='city',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='continent',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 12, 19, 1, 48, 747013, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='post_part_1',
            field=models.CharField(default=None, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='post_part_2',
            field=models.CharField(default=None, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='subtitle',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='video_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
