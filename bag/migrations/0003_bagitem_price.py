# Generated by Django 5.0.2 on 2024-02-14 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bag', '0002_bagitem_subtotal_alter_bagitem_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
