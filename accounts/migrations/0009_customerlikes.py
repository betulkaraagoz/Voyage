# Generated by Django 3.1 on 2020-09-02 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0028_auto_20200902_1431'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_delete_userprofilephoto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodation.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]