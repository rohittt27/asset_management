# Generated by Django 4.1.7 on 2023-03-20 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry', '0033_alter_assignasset_date_of_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignasset',
            name='date_of_assign',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]