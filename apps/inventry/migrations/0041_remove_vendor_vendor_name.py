# Generated by Django 3.2.11 on 2023-08-07 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0040_alter_asset_serial_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_name',
        ),
    ]
