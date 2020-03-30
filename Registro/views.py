from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages, auth
from Cms.models import Cms, Cms_Slider
from .models import Projeto, Registro
from Equipamento.models import Equipamento, Equip_Projeto
from Cliente.models import Vendedor, Revenda, Cliente_Final, Revenda_User
from django.contrib.auth.models import User
from django.core.validators import validate_email


class RegistroIndex(View):
    model = 'Registro'
    template_name = 'Registro/index.html'
    cms_id = Cms.objects.latest('pk')
    files = Cms_Slider.objects.filter(cms=cms_id)
    revendas = Revenda.objects.all()
    vendedores = Vendedor.objects.all()

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.id_user = request.user.id
        if self.id_user:
            self.vendedor_user = Vendedor.objects.get(user_vendedor=self.id_user).is_gerente
            self.registros_att = Registro.objects.filter(atualizado=False)
            self.count_registro = len(self.registros_att)
        else:
            self.vendedor_user = None
            self.registros_att = None
            self.count_registro = None
        self.contexto = {
            'number_registro': self.count_registro,
            'vendedor_gerente': self.vendedor_user,
            'revendas': self.revendas,
            'users': request.user.is_authenticated,
            'imgs': self.files,
            'vendedores': self.vendedores,
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        self.contexto = {
            'revendas': self.revendas,
            'users': request.user.is_authenticated,
            'imgs': self.files,
            'vendedores': self.vendedores,
            'cnpj_cliente': request.POST.get("cnpj_cliente"),
            'contact_cliente': request.POST.get("contact_cliente"),
            'razao_cliente': request.POST.get("razao_cliente"),
            'cep_cliente': request.POST.get("cep_cliente"),
            'address_cliente': request.POST.get("address_cliente"),
            'city_cliente': request.POST.get("city_cliente"),
            'state_cliente': request.POST.get("state_cliente"),
            'email_cliente': request.POST.get("email_cliente"),
            'phone_cliente': request.POST.get("phone_cliente"),
            'aplication_projeto': request.POST.get("aplication_projeto"),
            'esp_projeto': request.POST.get("esp_projeto"),
            'colet_projeto': request.POST.get("colet_projeto"),
            'info_projeto': request.POST.get("info_projeto"),
            'concl_projeto': request.POST.get("concl_projeto"),
            'vendedor': request.POST.get("vendedor"),
        }
        if request.POST.get('user'):
            if request.method != 'POST':
                return render(request, 'Registro/index.html')
            nome = request.POST.get('name')
            email = request.POST.get('email')
            usuario = request.POST.get('user')
            senha = request.POST.get('pwd')
            senha2 = request.POST.get('pwd2')
            revenda_user = int(request.POST.get('revendaRegister'))
            revenda_user_o = Revenda.objects.get(id=revenda_user)
            print(revenda_user_o)
            if not nome or not email or not senha or not senha2 or not usuario:
                messages.error(request, 'Campo Vazio!')
                return render(request, 'Registro/index.html')
            try:
                validate_email(email)
            except:
                messages.error(request, 'Email Invalido')
                return render(request,self.template_name, self.contexto)
            if len(senha) < 6:
                messages.error(request, 'Senha curta')
                return render(request, self.template_name, self.contexto)
            if len(usuario) < 4:
                messages.error(request, 'Usuario curto')
                return render(request, self.template_name, self.contexto)
            if senha != senha2:
                messages.error(request, 'Senhas não conferem!')
                return render(request, self.template_name, self.contexto)
            if User.objects.filter(username=usuario).exists():
                messages.error(request, 'Usuario já existe')
                return render(request, self.template_name, self.contexto)
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email já existe')
                return render(request, self.template_name, self.contexto)
            user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome)
            try:
                user.save()
            except:
                messages.error(request, 'Falha ao se cadastrar! Contacte o administrador do site!')
                return render(request, self.template_name, self.contexto)
            try:
                user_revenda = Revenda_User(nome=nome, revenda=revenda_user_o, user_revenda=user)
                user_revenda.save()
                messages.success(request, 'Cadastrado com sucesso!')
                return render(request, self.template_name, self.contexto)
            except:
                messages.error(request, 'Falha ao se cadastrar! Contacte o administrador do site!')
                return render(request, self.template_name, self.contexto)
        if request.POST.get("cnpj_cliente") == '':
            messages.error(request, 'Inserir o CNPJ do cliente')
            return render(request, self.template_name, self.contexto)
        try:
            id_cliente_b = Cliente_Final.objects.get(cnpj=request.POST.get("cnpj_cliente"))
        except:
            cnpj_cliente = request.POST.get("cnpj_cliente")
            razao_cliente = request.POST.get("razao_cliente")
            address_cliente = request.POST.get("address_cliente")
            city_cliente = request.POST.get("city_cliente")
            state_cliente = request.POST.get("state_cliente")
            email_cliente = request.POST.get("email_cliente")
            phone_cliente = request.POST.get("phone_cliente")
            cep_cliente = request.POST.get("cep_cliente")
            if razao_cliente == '' or address_cliente == '' or city_cliente == '' or state_cliente == '' or email_cliente == '' or phone_cliente == '':
                messages.error(request, 'Inserir informações do cliente')
                return render(request, self.template_name, self.contexto)
            cliente = Cliente_Final(cep=cep_cliente ,razao_social=razao_cliente, cnpj=cnpj_cliente, rua=address_cliente, cidade=city_cliente, estado=state_cliente, telefone=phone_cliente, email=email_cliente)
            try:
                cliente.save()
                id_cliente_b = cliente
            except:
                messages.error(request, 'Erro ao cadastrar Cliente!! Contate o administrador do site!')
                return render(request, self.template_name, self.contexto)

        if request.user.is_authenticated:
            self.id_user = request.user
            self.revenda_user_id = Revenda_User.objects.get(user_revenda=self.id_user)
            self.revenda_id = Revenda.objects.get(pk=self.revenda_user_id.revenda.id)
            revenda_id_b = self.revenda_id
            print(revenda_id_b)
        else:
            try:
                cnpj_revenda = request.POST.get("cnpj_revenda")
                self.revenda_id = Revenda.objects.get(cnpj=cnpj_revenda)
                revenda_id_b = self.revenda_id
            except:
                cnpj_revenda = request.POST.get("cnpj_revenda")
                razao_revenda = request.POST.get("razao_revenda")
                address_revenda = request.POST.get("address_revenda")
                city_revenda = request.POST.get("city_revenda")
                state_revenda = request.POST.get("state_revenda")
                email_revenda = request.POST.get("email_revenda")
                phone_revenda = request.POST.get("phone_revenda")
                cep_revenda = request.POST.get("cep_revenda")
                revenda = Revenda(cep=cep_revenda, razao_social=razao_revenda, cnpj=cnpj_revenda, rua=address_revenda, cidade=city_revenda, estado=state_revenda, telefone=phone_revenda, email=email_revenda)
                try:
                    revenda.save()
                    revenda_id_b = revenda
                except:
                    messages.error(request, 'Erro ao cadastrar Revenda!! Contate o administrador do site!')
        aplication_projeto = request.POST.get("aplication_projeto")
        esp_projeto = request.POST.get("esp_projeto")
        homologa_projeto = request.POST.get("homologa_projeto")
        if homologa_projeto == 'sim':
            homologa_projeto=True
        else:
            homologa_projeto=False

        colet_projeto = request.POST.get("colet_projeto")
        parc_projeto = request.POST.get("parc_projeto")
        concl_projeto = request.POST.get("concl_projeto")
        info_projeto = request.POST.get("info_projeto")
        if aplication_projeto == '' or esp_projeto == '' or colet_projeto == '' or parc_projeto == '' or concl_projeto == '':
            messages.error(request, 'Inserir informações do Projeto')
            return render(request, self.template_name, self.contexto)
        projeto = Projeto(aplicacao=aplication_projeto, esp_tec=esp_projeto, homologa=homologa_projeto, colet_dados=colet_projeto, parc_soft=parc_projeto, info_ad=info_projeto, date_concl=concl_projeto)
        try:
            projeto.save()
            projeto_id = projeto
        except:
            messages.error(request, 'Erro ao cadastrar Projeto!! Contate o administrador do site!')
            return render(request, self.template_name, self.contexto)

        for i in range(10000):
            if request.POST.get(f'pn_projeto{i}'):
                pn = request.POST.get(f'pn_projeto{i}')
                descr = request.POST.get(f'desc_projeto{i}')
                qty = request.POST.get(f'qty_projeto{i}')
                value = request.POST.get(f'value_projeto{i}')
                equipamento = Equipamento(pn=pn, descricao=descr)
                try:
                    equipamento.save()
                except:
                    messages.error(request, 'Erro ao cadastrar Produto!! Contate o administrador do site!')
                equip_proj = Equip_Projeto(id_projeto=projeto_id, id_equip=equipamento, valor=value, qty=qty)
                try:
                    equip_proj.save()
                except:
                    messages.error(request, 'Erro ao cadastrar Produto!! Contate o administrador do site!')
            else:
                break

        for j in range(10000):
            if request.POST.get(f'ac_pn_projeto{j}'):
                pn = request.POST.get(f'ac_pn_projeto{j}')
                descr = request.POST.get(f'ac_desc_projeto{j}')
                qty = request.POST.get(f'ac_qty_projeto{j}')
                value = request.POST.get(f'ac_value_projeto{j}')
                equipamento = Equipamento(pn=pn, descricao=descr, is_acessorio=True)
                try:
                    equipamento.save()
                except:
                    messages.error(request, 'Erro ao cadastrar Acessório!! Contate o administrador do site!')
                equip_proj = Equip_Projeto(id_projeto=projeto_id, id_equip=equipamento, valor=value, qty=qty)
                try:
                    equip_proj.save()
                except:
                    messages.error(request, 'Erro ao cadastrar Acessório!! Contate o administrador do site!')
            else:
                break

        contact_cliente = request.POST.get("contact_cliente")
        id_vendedor_b = request.POST.get("vendedor")
        id_vendedor = Vendedor.objects.get(id=id_vendedor_b)
        registro = Registro(id_revenda=revenda_id_b, id_revenda_user=self.revenda_user_id, id_cliente=id_cliente_b, id_projeto=projeto_id, id_vendedor=id_vendedor, contato=contact_cliente)
        try:
            registro.save()
            messages.success(request, 'Registro efetuado com sucesso!!')
        except:
            messages.error(request, 'Erro ao cadastrar Registro!! Contate o administrador do site!')
            return render(request, self.template_name, self.contexto)
        """ url = 'http://homologa.crm.primeinterway.com.br:808/suitecrm/service/v4_1/rest.php'
        paramters = {
            'method': 'POST',
            'input_type': 'JSON',
            'response_type': 'JSON',
            'rest_data': {
                'module': 'Opportunity',
                'name_value_list': {
                    {
                        'name': id_cliente_b + '/RegistroOportunidade',
                    }
                }
            }
        }
        jsonE = json.dumps(paramters)
        postArgs = 'method=set_entry&input_type=JSON&response_type=JSON&rest_data='+jsonE
        c = pycurl.Curl()
        c.setopt(c.URL, url)"""

        return redirect('index')


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('email')
    senha = request.POST.get('pwd')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return redirect('index')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso.')
        return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')
