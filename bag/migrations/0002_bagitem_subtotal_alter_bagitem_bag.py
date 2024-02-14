# Generated by Django 5.0.2 on 2024-02-14 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='bagitem',
            name='bag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bag.bag'),
        ),
    ]
