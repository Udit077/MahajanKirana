# Generated by Django 3.0.3 on 2021-04-18 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_remove_products_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='Status',
            field=models.CharField(default='Available', max_length=20),
        ),
    ]