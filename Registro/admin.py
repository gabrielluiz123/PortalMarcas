from django.contrib import admin
from .models import Registro, Projeto


class RegistroAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_revenda_user', 'id_revenda', 'id_cliente', 'status', 'id_vendedor', 'date_entered')
    list_display_links = ('id',)


class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id', 'homologa', 'parc_soft')
    list_display_links = ('id',)
    search_fields = ('aplicacao', 'esp_tec', 'colet_dados', 'info_ad')


admin.site.register(Registro, RegistroAdmin)
admin.site.register(Projeto, ProjetoAdmin)
