# Generated by Django 2.2.3 on 2020-03-11 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0006_auto_20200311_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenda',
            name='user_revenda',
        ),
    ]
