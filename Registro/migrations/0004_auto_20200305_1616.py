# Generated by Django 2.2.3 on 2020-03-05 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0003_auto_20200305_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='parc_soft',
            field=models.CharField(max_length=255, verbose_name='Parceiro de software'),
        ),
    ]
