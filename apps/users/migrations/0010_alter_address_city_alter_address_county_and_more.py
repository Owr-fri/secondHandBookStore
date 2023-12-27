# Generated by Django 4.1.3 on 2023-01-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_address_region_address_city_address_county_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(default=1, max_length=15, verbose_name='市'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(default=2000, max_length=15, verbose_name='区'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(default='a', max_length=15, verbose_name='省份'),
            preserve_default=False,
        ),
    ]
