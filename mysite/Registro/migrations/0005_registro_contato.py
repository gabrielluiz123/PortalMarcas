# Generated by Django 2.2.3 on 2020-03-12 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0004_auto_20200305_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='contato',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Contato Cliente'),
        ),
    ]
