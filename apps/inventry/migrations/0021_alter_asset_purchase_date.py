# Generated by Django 4.1.5 on 2023-02-21 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0020_asset_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
