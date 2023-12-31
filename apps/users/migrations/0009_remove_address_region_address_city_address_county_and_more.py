# Generated by Django 4.1.3 on 2023-01-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='region',
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='市'),
        ),
        migrations.AddField(
            model_name='address',
            name='county',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='区'),
        ),
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='省份'),
        ),
    ]
