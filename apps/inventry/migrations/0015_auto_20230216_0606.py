# Generated by Django 2.2.12 on 2023-02-16 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0014_assignasset_date_of_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignasset',
            name='date_of_assign',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]