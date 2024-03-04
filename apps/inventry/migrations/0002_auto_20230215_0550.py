# Generated by Django 2.2.12 on 2023-02-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientasset',
            name='date_of_dispatch',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clientasset',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clientasset',
            name='is_dispatch',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
