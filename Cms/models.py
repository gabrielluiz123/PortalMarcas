from django.db import models
from PIL import Image
from django.conf import settings
import os


class Cms(models.Model):
    marca = models.CharField(max_length=150,verbose_name='Marca')
    img_header = models.ImageField(verbose_name='Imagem Cabeçalho')
    img_form = models.ImageField(upload_to='imgs/img_header', blank=True, null=True, verbose_name='Imagem Formulário')
    text_sobre = models.TextField(verbose_name='Texto sobre')

    def __str__(self):
        return self.marca


class Cms_Slider(models.Model):
    cms = models.ForeignKey(Cms, on_delete=models.DO_NOTHING)
    img_slider = models.ImageField(upload_to='imgs/img_slider', blank=True, null=True, verbose_name='Imagem Slider')
    descricao = models.TextField(verbose_name='Descrição da Imagem')

    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image(self.img_slider.name, 200)

    @staticmethod
    def resize_image(nome_imagem, nova_altura):
        img_path = os.path.join(settings.MEDIA_ROOT, nome_imagem)
        img = Image.open(img_path)
        nova_img = img.resize((200, 350), Image.ANTIALIAS)
        nova_img.save(
            img_path,
            optimize=True,
            quality=100
        )
        nova_img.close()