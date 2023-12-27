# Generated by Django 4.1.3 on 2023-02-10 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitems_cart_alter_orderitems_goods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='returns',
        ),
        migrations.AddField(
            model_name='orders',
            name='cancel',
            field=models.BooleanField(default=False, verbose_name='已取消'),
        ),
    ]
