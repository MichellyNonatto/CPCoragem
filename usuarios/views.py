from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.utils.datetime_safe import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView, UpdateView, ListView, DeleteView, CreateView

from usuarios.regra import Funcionamento, Acesso
from usuarios.models import Funcionario, Usuario, Endereco, Pagamento, RegistroPagamento
from usuarios.forms import RecuperarContaForm, AutenticacaoContaForm, CriarFuncionarioForm, AutenticacaoClienteForm


class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            dashboard_url = reverse_lazy('usuarios:dashboard', kwargs={'pk': self.request.user.pk})
            return dashboard_url

        return super().get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)

        conta = Acesso()
        if not conta.get_acesso_conta(self.request.user):
            messages.error(self.request, "E-mail ou senha inválidos. Por favor, verifique suas informações de login.")
            logout(self.request)
            return self.form_invalid(form)

        return response


class RecuperarConta(FormView):
    template_name = 'recuperarconta.html'
    form_class = RecuperarContaForm

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            usuario = usuarios.first()
            if usuario.categoria == 'FUNCIONARIO':
                return reverse('usuarios:autenticacao', args=[usuario.pk])
        messages.error(self.request, 'Não encontramos um registro correspondente ao e-mail fornecido. '
                                     'Verifique se você digitou corretamente ou entre em contato com o suporte.')
        return reverse('usuarios:recuperarconta')


class Autenticacao(FormView):
    template_name = "autenticacao.html"
    form_class = AutenticacaoContaForm

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return messages.error('Código de autenticação fornecido é inválido.')
        return reverse('usuarios:atualizarsenha', args=[pk])


class AtualizarSenha(UpdateView):
    template_name = "autenticacao.html"
    model = Usuario
    fields = ['password']

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('usuarios:login')


class Dashboard(LoginRequiredMixin, DetailView):
    template_name = 'dashboard.html'
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user
        funcionario = Funcionario.objects.get(usuario=usuario)
        mensagem = Funcionamento.mensagem()
        context['mensagem'] = mensagem
        context['funcionario'] = funcionario
        return context


class EditarPerfilUsuario(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['nome_completo', 'telefone']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        usuario = Usuario.objects.get(pk=user.pk)
        context['usuario'] = usuario.pk
        context['endereco'] = usuario.endereco.pk
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        dashboard_url = reverse_lazy('usuarios:dashboard', kwargs={'pk': self.request.user.pk})
        return dashboard_url


class EditarPerfilEndereco(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Endereco
    fields = ['cep', 'estado', 'cidade', 'bairro', 'rua', 'numero', 'complemento']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        endereco_pk = self.kwargs['pk']
        usuario = Usuario.objects.get(endereco_id=endereco_pk)
        context['usuario'] = usuario.pk
        context['endereco'] = endereco_pk
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        dashboard_url = reverse_lazy('usuarios:dashboard', kwargs={'pk': self.request.user.pk})
        return dashboard_url


class ListaFuncionarios(LoginRequiredMixin, ListView):
    template_name = 'listafuncionarios.html'
    model = Funcionario

    def get(self, request, *args, **kwargs):
        funcionarios = Funcionario.objects.filter(usuario=self.request.user)
        for funcionario in funcionarios:
            if funcionario.funcao.descricao != 'Gerente':
                return HttpResponse("<h1>Sem contexto (204)</h1>")
            return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_atual'] = self.request.user
        return context


class PesquisaFuncionarios(LoginRequiredMixin, ListView):
    template_name = "listafuncionarios.html"
    model = Funcionario

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")

        if not termo_pesquisa or termo_pesquisa.isspace():
            return Funcionario.objects.none()

        resultados_funcionarios = Funcionario.objects.filter(
            Q(usuario__first_name__icontains=termo_pesquisa) |
            Q(usuario__last_name__icontains=termo_pesquisa) |
            Q(usuario__documento__icontains=termo_pesquisa) |
            Q(funcao__descricao__icontains=termo_pesquisa)
        )

        return resultados_funcionarios

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['termo_pesquisa'] = self.request.GET.get("query")
        context['usuario_atual'] = self.request.user
        return context


class VerFuncionario(LoginRequiredMixin, DetailView):
    template_name = 'verfuncionario.html'
    model = Funcionario


class EditarFuncionario(LoginRequiredMixin, UpdateView):
    template_name = "verfuncionario.html"
    model = Funcionario
    fields = ['turno', 'funcao']

    def form_valid(self, form):
        form.save()
        success_url = reverse('usuarios:listafuncionarios') + '?mensagem=Alteração em funcionário salva com sucesso!'
        return redirect(success_url)

    def get_success_url(self):
        verfuncionario_url = reverse_lazy('usuarios:verfuncionario', kwargs={'pk': self.object.pk})
        return verfuncionario_url


class DeletarFuncionario(LoginRequiredMixin, DeleteView):
    template_name = 'deletarfuncionario.html'
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario_pk = Funcionario.objects.get(usuario_id=self.object.pk)
        context['funcionario_pk'] = funcionario_pk.pk
        return context

    def get_success_url(self):
        return reverse('usuarios:listafuncionarios')


class AdicionarFuncionario(LoginRequiredMixin, FormView):
    template_name = "adicionarfuncionario.html"
    form_class = CriarFuncionarioForm

    def form_valid(self, form):
        documento = form.cleaned_data['documento']
        if Usuario.objects.filter(documento=documento).exists():
            messages.error(self.request, 'Funcionário já existe em nossa base de dados.')
        else:
            form.save()
            success_url = reverse('usuarios:listafuncionarios') + '?mensagem=Funcionário adicionado com sucesso!'
            return redirect(success_url)

        return reverse('usuarios:adicionarfuncionario')


class AutenticacaoClienteView(FormView):
    template_name = "autenticacaocliente.html"
    form_class = AutenticacaoClienteForm

    def get_success_url(self):
        email = self.request.POST.get("email")
        documento = self.request.POST.get("documento")
        try:
            usuario = Usuario.objects.get(email=email, documento=documento)

            if usuario.categoria == 'TUTOR':
                try:
                    pagamento = Pagamento.objects.filter(cliente=usuario)
                    pagamento = pagamento.first()
                    return reverse('usuarios:atualizarpagamento', args=[usuario.pk])
                except Pagamento.DoesNotExist:
                    messages.error(self.request, 'Não há registro de pagamento para este usuário.')
        except Usuario.DoesNotExist:
            messages.error(self.request, 'Não encontramos um registro correspondente ao e-mail fornecido. '
                                         'Verifique seu endereço de e-mail e número de documento para acessar a página de documento.')

        return reverse('usuarios:autenticacaocliente')


class CriarNovoPagamento(CreateView):
    template_name = "autenticacaocliente.html"
    model = RegistroPagamento
    fields = ['tipo']

    def form_valid(self, form):
        user = self.kwargs['pk']
        try:
            pagamento = Pagamento.objects.exclude(registropagamento__isnull=False)
        except Pagamento.DoesNotExist:
            return redirect('error_page')

        registro_pagamento = form.save(commit=False)

        pagamento = pagamento.filter(cliente=user).first()
        registro_pagamento.total_pago = pagamento.total_pagamento
        registro_pagamento.pagamento = pagamento
        registro_pagamento.pagamento = pagamento
        user_instance = Usuario.objects.get(pk=user)
        registro_pagamento.dia_pagamento = timezone.now()

        Pagamento.objects.create(
            cliente=Usuario.objects.get(pk=user),
            dia_vencimento=pagamento.dia_vencimento + relativedelta(months=1),
            total_pagamento=pagamento.total_pagamento
        )

        registro_pagamento.save()
        success_url = reverse('usuarios:autenticacaocliente') + '?mensagem=Pagamento efetuado com sucesso!'
        return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_formulario = 'pagamento'
        context['tipo'] = tipo_formulario
        return context


class ListaPagamentos(LoginRequiredMixin, ListView):
    template_name = "listapagamento.html"

    def __init__(self):
        self.hoje = datetime.now().date()

    def get_queryset(self):
        queryset = Pagamento.objects.exclude(registropagamento__isnull=False).filter(
            dia_vencimento__lt=self.hoje).order_by(
            'dia_vencimento')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vencido_list = []
        for pagamento in self.object_list:
            if pagamento.dia_vencimento <= self.hoje:
                qtd = self.hoje - pagamento.dia_vencimento
                dias_corridos = {'id': pagamento.pk, 'dias': qtd.days}
                vencido_list.append(dias_corridos)

        context['usuario_atual'] = self.request.user
        context['dias_corridos'] = vencido_list
        return context


class PesquisarPagamento(ListaPagamentos):
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")

        if not termo_pesquisa or termo_pesquisa.isspace():
            return Pagamento.objects.none()

        resultados_tutores = Pagamento.objects.filter(
            Q(cliente__nome_completo__icontains=termo_pesquisa) |
            Q(cliente__documento__icontains=termo_pesquisa) |
            Q(cliente__endereco__cidade__icontains=termo_pesquisa) |
            Q(cliente__endereco__cep__icontains=termo_pesquisa) |
            Q(cliente__email__icontains=termo_pesquisa) |
            Q(cliente__telefone__icontains=termo_pesquisa)

        )
        pagamento = resultados_tutores.exclude(registropagamento__isnull=False)
        return pagamento


class DeletarCliente(LoginRequiredMixin, DeleteView):
    template_name = 'deletarcliente.html'
    model = Usuario
    def get_success_url(self):
        return reverse('usuarios:listafuncionarios')