# Generated by Django 2.1 on 2019-05-14 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20190513_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingstats',
            name='reads',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='readingstats',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
