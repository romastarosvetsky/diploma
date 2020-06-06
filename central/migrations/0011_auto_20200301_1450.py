# Generated by Django 2.2.6 on 2020-03-01 14:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('central', '0010_auto_20200229_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='load',
            name='result_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Result value'),
        ),
    ]