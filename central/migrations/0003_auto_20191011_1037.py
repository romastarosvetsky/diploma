# Generated by Django 2.2.6 on 2019-10-11 10:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0002_auto_20191008_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 11, 10, 37, 31, 654110, tzinfo=utc), verbose_name='Created at'),
        ),
    ]
