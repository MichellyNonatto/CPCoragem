import random
from django import forms
from unidecode import unidecode
from django.utils.datetime_safe import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, Funcionario, Endereco, Funcao, Pagamento


class RecuperarContaForm(forms.Form):
    email = forms.EmailField()


class AutenticacaoContaForm(forms.Form):
    codigo = forms.CharField(max_length=15)

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        try:
            usuario = Usuario.objects.get(documento=codigo)
        except Usuario.DoesNotExist:
            raise forms.ValidationError('Código de autenticação fornecido é inválido.')
        return codigo


class CriarUsuario(UserCreationForm):
    random_password = f'{random.randint(1000, 9999)}7b#T!pM$&W5uLqX9'
    password1 = forms.CharField(label='password1', widget=forms.HiddenInput, initial=random_password)
    password2 = forms.CharField(label='password2', widget=forms.HiddenInput, initial=random_password)

    nome_completo = forms.CharField(max_length=100, label='Nome Completo')
    cep = forms.IntegerField()
    estado = forms.CharField(max_length=45)
    cidade = forms.CharField(max_length=45)
    bairro = forms.CharField(max_length=45)
    rua = forms.CharField(max_length=45)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=45, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        primeiro_nome = self.cleaned_data.get('nome_completo', '').split()
        primeiro_nome = unidecode(primeiro_nome[0].lower())

        user.username = f'{primeiro_nome}{random.randint(1000, 9999)}'
        user.categoria = None
        user.set_password(f'{random.randint(1000, 9999)}7b#T!pM$&W5uLqX9')

        if commit:
            endereco, created = Endereco.objects.get_or_create(
                cep=self.cleaned_data['cep'],
                estado=self.cleaned_data['estado'],
                cidade=self.cleaned_data['cidade'],
                bairro=self.cleaned_data['bairro'],
                rua=self.cleaned_data['rua'],
                numero=self.cleaned_data['numero'],
                complemento=self.cleaned_data['complemento']
            )
            user.endereco = endereco
            user.save()

            return user

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'documento', 'email', 'telefone')


class CriarFuncionarioForm(CriarUsuario):
    imagem = forms.ImageField()
    turno = forms.ChoiceField(choices=Funcionario.TURNO_CHOICES, label="Turno")
    funcao = forms.ModelChoiceField(queryset=Funcao.objects.all(), label="Função")

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'documento', 'telefone')

    def save(self, commit=True):
        user = super().save()
        user.categoria = 'FUNCIONARIO'
        user.email = f'{user.username}@coragem.com.br'
        user.categoria = 'FUNCIONARIO'

        if commit:
            Funcionario.objects.create(
                imagem=self.cleaned_data['imagem'],
                turno=self.cleaned_data['turno'],
                funcao=self.cleaned_data['funcao'],
                usuario=user
            )
            user.save()
        return user


class CriarTutorForm(CriarUsuario):
    def save(self, commit=True):
        user = super().save()
        user.categoria = 'TUTOR'

        if commit:
            Pagamento.objects.create(
                cliente=user,
                total_pagamento= 0,
                dia_vencimento=datetime.now().date() + relativedelta(months=1)
            )
            user.save()

        return user


class AutenticacaoClienteForm(forms.Form):
    email = forms.EmailField(max_length=255)
    documento = forms.CharField(max_length=15)
