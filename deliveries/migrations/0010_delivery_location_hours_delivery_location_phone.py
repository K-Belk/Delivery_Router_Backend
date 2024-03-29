# Generated by Django 4.0.4 on 2022-09-18 14:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0009_alter_deliveries_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_location',
            name='hours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delivery_location',
            name='phone',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
