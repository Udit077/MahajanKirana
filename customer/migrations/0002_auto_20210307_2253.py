# Generated by Django 3.0.3 on 2021-03-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='Discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='Price',
            field=models.IntegerField(default=''),
        ),
    ]
