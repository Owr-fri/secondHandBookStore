# Generated by Django 4.1.3 on 2022-12-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(0, '女性'), (1, '男性')], default=1),
        ),
    ]
