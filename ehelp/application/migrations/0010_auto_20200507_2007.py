# Generated by Django 3.0.2 on 2020-05-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_auto_20200507_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='supply',
            field=models.BooleanField(default=0),
        ),
    ]