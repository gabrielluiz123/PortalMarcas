from django.db import models
from django.utils import timezone
from Registro.models import Projeto


class Equipamento(models.Model):
    pn = models.CharField(max_length=150, verbose_name='Part Number')
    descricao = models.TextField(verbose_name='Descrição')
    is_acessorio = models.BooleanField(default=False, verbose_name="Acessório")
    date_entered = models.DateTimeField(default=timezone.now, verbose_name='Data de Entrada')

    def __str__(self):
        return self.pn


class Equip_Projeto(models.Model):
    name = models.CharField(max_length=150, default='Equip')
    id_projeto = models.ForeignKey(Projeto, on_delete=models.DO_NOTHING, verbose_name='Projeto')
    id_equip = models.ForeignKey(Equipamento, on_delete=models.DO_NOTHING, verbose_name='Equipamento')
    valor = models.FloatField(verbose_name='Valor')
    qty = models.IntegerField(default=1,verbose_name='Quantidade')

    def __str__(self):
        return self.name