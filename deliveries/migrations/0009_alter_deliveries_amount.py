# Generated by Django 4.0.4 on 2022-09-17 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0008_alter_editionchoices_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveries',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]