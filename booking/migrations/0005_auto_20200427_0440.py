# Generated by Django 3.0.5 on 2020-04-27 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20200427_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurantsbooking', to='booking.Restaurant'),
        ),
    ]
