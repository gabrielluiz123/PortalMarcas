# Generated by Django 2.2.3 on 2020-03-16 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cliente', '0009_auto_20200312_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente_final',
            name='cep',
            field=models.CharField(default=12120000, max_length=255, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='revenda',
            name='cep',
            field=models.CharField(default=12120000, max_length=255, verbose_name='Cep'),
        ),
    ]
