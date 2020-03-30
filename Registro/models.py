from django.db import models
from django.utils import timezone
from Cliente.models import Revenda, Cliente_Final, Vendedor, Revenda_User


class Projeto(models.Model):
    aplicacao = models.TextField(verbose_name='Aplicação')
    esp_tec = models.TextField(verbose_name='Especificações Técnicas')
    homologa = models.BooleanField(default=False, verbose_name='Homologado')
    colet_dados = models.TextField(verbose_name='Coletor de dados')
    parc_soft = models.CharField(max_length=255, verbose_name='Parceiro de software')
    date_concl = models.DateTimeField(default=timezone.now, verbose_name='Data de Conclusão')
    info_ad = models.TextField(verbose_name='Informações adicionais')

    def __str__(self):
        return self.aplicacao


class Registro(models.Model):
    name = models.CharField(default='Registro Oportunidade', max_length=150, verbose_name='name')
    id_revenda = models.ForeignKey(Revenda, on_delete=models.DO_NOTHING, verbose_name='Revenda')
    id_revenda_user = models.ForeignKey(Revenda_User, on_delete=models.DO_NOTHING, verbose_name='Revenda Usuário', blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente_Final, on_delete=models.DO_NOTHING, verbose_name='Cliente Final')
    id_projeto = models.ForeignKey(Projeto, on_delete=models.DO_NOTHING, verbose_name='Projeto')
    id_vendedor = models.ForeignKey(Vendedor, on_delete=models.DO_NOTHING, verbose_name='Vendedor')
    date_entered = models.DateTimeField(default=timezone.now, verbose_name='Data de entrada')
    contato = models.CharField(max_length=255, verbose_name='Contato Cliente', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name='Status')
    atualizado = models.BooleanField(default=False, verbose_name='Atualizado')
    date_atualizado = models.DateField(verbose_name='Data Atualização', blank=True, null=True)
    numero_registro = models.CharField(max_length=150, verbose_name='Número de Registro', blank=True, null=True)

    def __str__(self):
        return self.name
