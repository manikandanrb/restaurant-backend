# Generated by Django 3.0.5 on 2020-04-27 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20200426_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]