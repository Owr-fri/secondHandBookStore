# Generated by Django 4.1.3 on 2023-02-26 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orders_courier_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='courier_number',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='courier_number',
            field=models.CharField(max_length=50, null=True, verbose_name='快递单号'),
        ),
    ]
