# Generated by Django 4.0.4 on 2022-09-15 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0006_editionchoices_productchoices_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveries',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]