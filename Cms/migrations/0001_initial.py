# Generated by Django 2.2.3 on 2020-03-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=150, verbose_name='Marca')),
                ('img_header', models.ImageField(upload_to='', verbose_name='Imagem Cabeçalho')),
                ('img_form', models.ImageField(blank=True, null=True, upload_to='imgs/img_header', verbose_name='Imagem Formulário')),
                ('text_sobre', models.TextField(verbose_name='Texto sobre')),
            ],
        ),
    ]
