# Generated by Django 3.2.11 on 2023-08-04 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0039_alter_vendor_vendor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='serial_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]