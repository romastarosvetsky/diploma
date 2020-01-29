# Generated by Django 2.2.6 on 2019-10-08 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('surname', models.CharField(max_length=64, verbose_name='Surname')),
                ('patronymic', models.CharField(blank=True, max_length=64, null=True, verbose_name='Patronymic')),
                ('faculty', models.CharField(blank=True, max_length=64, null=True, verbose_name='Faculty')),
                ('position', models.CharField(blank=True, max_length=64, null=True, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
    ]