# Generated by Django 4.1.7 on 2023-03-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0031_remove_assignasset_have_asset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientasset',
            name='date_of_dispatch',
            field=models.DateField(blank=True, null=True),
        ),
    ]
