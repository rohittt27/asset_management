# Generated by Django 2.2.12 on 2023-02-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0004_auto_20230215_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientasset',
            name='date_of_dispatch',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]
