import random

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.datetime_safe import datetime
from unidecode import unidecode

from .models import Endereco, Funcao, Funcionario, Pagamento, Usuario


class RecuperarContaForm(forms.Form):
    email = forms.EmailField()


class AutenticacaoContaForm(forms.Form):
    codigo = forms.CharField(max_length=15)

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        try:
            usuario = Usuario.objects.get(documento=codigo, pk=self.pk)
        except Usuario.DoesNotExist:
            raise forms.ValidationError(
                'Documento para a autenticação fornecido é inválido.')
        return codigo


class AtualizarSenhaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = []

    password1 = forms.CharField(
        label='Nova Senha', max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmar Senha', max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas estão diferentes.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.set_password(password)
        if commit:
            user.save()
        return user


class CriarUsuario(UserCreationForm):
    random_password = f'{random.randint(1000, 9999)}7b#T!pM$&W5uLqX9'
    password1 = forms.CharField(
        label='password1', widget=forms.HiddenInput, initial=random_password)
    password2 = forms.CharField(
        label='password2', widget=forms.HiddenInput, initial=random_password)

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
    funcao = forms.ModelChoiceField(
        queryset=Funcao.objects.all(), label="Função")

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
                total_pagamento=0,
                dia_vencimento=datetime.now().date() + relativedelta(months=1)
            )
            user.save()

        return user


class EditarUsuarioForm(UserChangeForm):
    cep = forms.IntegerField()
    estado = forms.CharField(max_length=45)
    cidade = forms.CharField(max_length=45)
    bairro = forms.CharField(max_length=45)
    rua = forms.CharField(max_length=45)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=45, required=False)

    class Meta:
        model = Usuario
        fields = ('nome_completo', 'telefone', 'email')

    def save(self, commit=True):
        endereco_data = {
            'cep': self.cleaned_data['cep'],
            'estado': self.cleaned_data['estado'],
            'cidade': self.cleaned_data['cidade'],
            'bairro': self.cleaned_data['bairro'],
            'rua': self.cleaned_data['rua'],
            'numero': self.cleaned_data['numero'],
            'complemento': self.cleaned_data['complemento'],
        }

        user = super().save(commit=False)

        if commit:
            if user.endereco:
                Endereco.objects.filter(
                    id=user.endereco.id).update(**endereco_data)
            else:
                endereco = Endereco.objects.create(**endereco_data)
                user.endereco = endereco

            user.save()

        return user


class AutenticacaoClienteForm(forms.Form):
    email = forms.EmailField(max_length=255)
    documento = forms.CharField(max_length=15)
