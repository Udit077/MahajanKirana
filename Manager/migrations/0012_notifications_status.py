# Generated by Django 3.0.3 on 2021-04-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0011_auto_20210418_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='Status',
            field=models.CharField(default='not_seen', max_length=10),
        ),
    ]
