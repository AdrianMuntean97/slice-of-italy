# Generated by Django 5.0.2 on 2024-02-15 01:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bag', '0003_bagitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bagitem',
            name='bag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bag_items', to='bag.bag'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='bag.bag')),
            ],
        ),
    ]