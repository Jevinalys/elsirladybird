# Generated by Django 5.0.3 on 2024-07-19 12:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsiruser', '0002_remove_customer_owner_remove_sale_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_paid',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
