from django.shortcuts import render, redirect
from django.views import View
from Registro.models import Projeto, Registro
from Cliente.models import Vendedor, Revenda, Revenda_User
from Equipamento.models import Equipamento, Equip_Projeto
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
import smtplib
import email.message

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class DetalheApphook(CMSApp):
    app_name = "detalhe"  # must match the application namespace
    name = "Detalhes"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["Detalhes.urls"]

class DetalhesIndex(View):
    model = 'Registro'
    template_name = 'Detalhes/index.html'
    vendedores = Vendedor.objects.all()

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.META['HTTP_HOST'] == 'bluebird.portal.com.br:8000':
            self.empresa = 'bluebird'
        elif request.META['HTTP_HOST'] == 'chainway.portal.com.br:8000':
            self.empresa = 'chainway'
        self.id_user = request.user
        try:
            self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        except:
            self.vendedor_user = None
        self.registros_att = Registro.objects.filter(atualizado=False)
        self.count_registro = len(self.registros_att)
        if self.vendedor_user:
            self.registro = Registro.objects.filter(marca=self.empresa).order_by('-date_entered')
        else:
            try:
                self.revenda_user_id = Revenda_User.objects.filter(user_revenda=self.id_user).first()
                if self.revenda_user_id.is_admin:
                    self.revenda = Revenda.objects.filter(revenda_user__user_revenda=self.id_user).first()
                    self.registro = Registro.objects.filter(id_revenda=self.revenda, marca=self.empresa).order_by('-date_entered')
                else:
                    self.registro = Registro.objects.filter(id_revenda_user=self.revenda_user_id, marca=self.empresa).order_by('-date_entered')
            except:
                self.id_vendedor_id = Vendedor.objects.filter(user_vendedor=self.id_user).first()
                self.registro = Registro.objects.filter(id_vendedor=self.id_vendedor_id, marca=self.empresa).order_by('-date_entered')
        page = request.GET.get('page', 1)
        paginator = Paginator(self.registro, 6)
        try:
            self.registro = paginator.page(page)
        except PageNotAnInteger:
            self.registro = paginator.page(1)
        except EmptyPage:
            self.registro = paginator.page(paginator.num_pages)

        self.contexto = {
            'empresa': self.empresa,
            'number_registro': self.count_registro,
            'vendedor_gerente': self.vendedor_user,
            'vendedor': self.vendedor_user,
            'users': self.registro,
            'registros': self.registro,
            'user': request.user.is_authenticated,
            'vendedores': self.vendedores,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class DetalheIndex(View):
    template_name = 'Detalhes/detalhe.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.id_user = request.user
        self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        self.revenda_user_id = Revenda_User.objects.get(user_revenda=self.id_user)
        pk = self.kwargs.get('pk')
        if request.META['HTTP_HOST'] == 'bluebird.portal.com.br:8000':
            self.empresa = 'bluebird'
        elif request.META['HTTP_HOST'] == 'chainway.portal.com.br:8000':
            self.empresa = 'chainway'
        try:
            if not self.vendedor_user:
                self.registro = Registro.objects.get(id_revenda_user=self.revenda_user_id, pk=pk, marca=self.empresa)
            else:
                self.registro = Registro.objects.get(pk=pk)
            self.id_projeto = self.registro.id_projeto
            self.pns = Equip_Projeto.objects.filter(id_projeto=self.id_projeto)
            self.i = self.j = None
            for self.pn in self.pns:
                if self.pn.id_equip.is_acessorio:
                    self.j = 1
                else:
                    self.i = 1
        except:
            self.registro = None

        self.contexto = {
            'empresa': self.empresa,
            'is_gerente': self.vendedor_user,
            'i': self.i,
            'j': self.j,
            'registro': self.registro,
            'pnss': self.pns,
            'users': request.user.is_authenticated,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class PostBusca(View):
    template_name = 'Detalhes/busca.html'
    model = 'Registro'
    vendedores = Vendedor.objects.all()

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        termo = self.request.GET.get('termo')
        self.id_user = request.user
        self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        self.registros_att = Registro.objects.filter(atualizado=False, marca=self.empresa)
        self.count_registro = len(self.registros_att)
        if self.vendedor_user:
            qs = Registro.objects.filter(
                Q(id_revenda__razao_social__icontains=termo) | Q(id_cliente__razao_social__icontains=termo)
            ).order_by('-date_entered')
        else:
            self.revenda_user_id = Revenda_User.objects.get(user_revenda=self.id_user)
            if self.revenda_user_id.is_admin:
                self.revenda = Revenda.objects.filter(revenda_user__user_revenda=self.id_user).first()
                self.registro = Registro.objects.filter(id_revenda=self.revenda, marca=self.empresa).order_by('-date_entered')
            else:
                self.registro = Registro.objects.filter(id_revenda_user=self.revenda_user_id, marca=self.empresa)
            qs = Registro.objects.filter(
                Q(id_revenda__razao_social__icontains=termo) | Q(id_cliente__razao_social__icontains=termo)
            ).filter(id_revenda_user=self.revenda_user_id).order_by('-date_entered')
        page = request.GET.get('page', 1)
        paginator = Paginator(qs, 6)
        try:
            self.registro = paginator.page(page)
        except PageNotAnInteger:
            self.registro = paginator.page(1)
        except EmptyPage:
            self.registro = paginator.page(paginator.num_pages)
        if request.META['HTTP_HOST'] == 'bluebird.portal.com.br:8000':
            self.empresa = 'bluebird'
        elif request.META['HTTP_HOST'] == 'chainway.portal.com.br:8000':
            self.empresa = 'chainway'
        self.contexto = {
            'empresa': self.empresa,
            'vendedor_gerente': self.vendedor_user,
            'number_registro': self.count_registro,
            'vendedor': self.vendedor_user,
            'termo': termo,
            'registros': self.registro,
            'users': request.user.is_authenticated,
            'vendedores': self.vendedores,
            'filters': qs,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)


class Aprovar(DetalhesIndex):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        if self.vendedor_user:
            self.pk = self.kwargs.get('pk')
            self.numero = request.POST.get("numero_registro")
            self.registro_update = Registro.objects.get(pk=self.pk)
            self.registro_update.atualizado = True
            self.registro_update.status = True
            self.registro_update.date_atualizado = timezone.now()
            self.registro_update.numero_registro = self.numero
            try:
                self.registro_update.save()
                messages.success(request, 'Aprovado com sucesso!!')
            except:
                messages.error(request, 'Falha ao Aprovar.')
            self.enviaEmail()
            return render(request, self.template_name, self.contexto)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def enviaEmail(self):
        self.url = "127.0.0.1:8000"
        self.url2 = f'/Detalhes/Detalhe/{self.pk}'
        self.url3 = self.url+self.url2
        print(self.url3)
        server = smtplib.SMTP('smtp.gmail.com:587')
        email_content = f'Registro para o cliente {self.registro_update.id_cliente} foi aprovado <br> Numero do Registro: {self.registro_update.numero_registro} <br> <a data-saferedirecturl="{self.url3}" href="{self.url3}">Link para o Registro</a>'
        msg = email.message.Message()
        msg['Subject'] = 'Registro de Oportunidade BlueBird Aprovado'

        msg['From'] = 'gabriel.santos@primeinterway.com.br'
        msg['To'] = 'gabriel.santos@primeinterway.com.br'
        password = "fordprefect@123"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)

        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        return


class Reprovar(DetalhesIndex):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        if self.vendedor_user:
            pk = self.kwargs.get('pk')
            self.numero = request.POST.get("numero_registro")
            self.registro_update = Registro.objects.get(pk=pk)
            self.registro_update.atualizado = True
            self.registro_update.status = False
            self.registro_update.date_atualizado = timezone.now()
            try:
                self.registro_update.save()
                messages.success(request, 'Reprovado com sucesso!!')
                self.enviaEmail()
            except:
                messages.error(request, 'Falha ao Aprovar.')

    def get_queryset(self):
        self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
        qs = super().get_queryset()
        return qs

    def enviaEmail(self):
        self.url = f'127.0.0.1:8000/Detalhes/Detalhe/{self.pk}'
        server = smtplib.SMTP('smtp.gmail.com:587')
        email_content = f'Registro para o cliente {self.registro_update.id_cliente} foi reprovado <br> <a href="{self.url}">Link: </a>'
        msg = email.message.Message()
        msg['Subject'] = 'Registro de Oportunidade BlueBird Reprovado'

        msg['From'] = 'gabriel.santos@primeinterway.com.br'
        msg['To'] = 'gabriel.santos@primeinterway.com.br'
        password = "fordprefect@123"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)

        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        return
