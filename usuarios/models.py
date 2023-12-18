from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2, blank=True)
    cidade = models.CharField(max_length=45, blank=True)
    bairro = models.CharField(max_length=45)
    rua = models.CharField(max_length=45)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return f'Cidade de {self.cidade}, {self.estado}'


def validar_tamanho_documento(value):
    if len(value) not in [7, 9, 11, 12]:
        raise ValidationError("Insira um documento válido.")


class Usuario(AbstractUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, default="+55 11")
    documento = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(7),
            MaxLengthValidator(14),
            validar_tamanho_documento,
            RegexValidator(
                regex=r'^\d+$',
                message='O número do documento deve conter apenas números.',
                code='invalid_documento'
            )
        ]
    )

    CATEGORIA_CHOICES = [
        ("FUNCIONARIO", "Funcionário"),
        ("TUTOR", "Tutor"),
    ]
    categoria = models.CharField(
        max_length=12, choices=CATEGORIA_CHOICES, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome_completo', 'documento']

    def get_documento_formatado(self):
        if len(self.documento) == 7:
            return ["CNH", f"XXX-{self.documento[3:]}"]
        elif 9 == len(self.documento) or len(self.documento) == 12:
            return ["RG",
                    f"XXX.{self.documento[2:5]}.{self.documento[5:9]}{f'-{self.documento[10:]}' if len(self.documento) == 12 else ''}"]
        else:
            return ["CPF", f"XXX.{self.documento[3:6]}.{self.documento[6:9]}-{self.documento[9:]}"]

    def get_endereco_formatado(self):
        return str(self.endereco)

    def __str__(self):
        return self.email


class Funcao(models.Model):
    descricao = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.descricao


class Funcionario(models.Model):
    imagem = models.ImageField(upload_to='imagens_funcionario/', default='blank-profile.webp')

    TURNO_CHOICES = [
        ("PRIMEIRO_TURNO", "1º Turno"),
        ("SEGUNDO_TURNO", "2º Turno"),
    ]
    turno = models.CharField(max_length=40, choices=TURNO_CHOICES)
    funcao = models.ForeignKey(
        Funcao, related_name="funcao", on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        Usuario, related_name="funcionarios", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.nome_completo} - {self.funcao.descricao}"

    def clean(self):
        if self.usuario.categoria != "FUNCIONARIO":
            raise ValidationError(
                "O usuário deve ter a categoria 'Funcionário' para ser associado a um funcionário.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Pagamento(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia_vencimento = models.DateField(default=timezone.now)
    total_pagamento = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.cliente.categoria != "TUTOR":
            raise ValidationError(
                "O usuário deve ter a categoria 'Tutor' para ser associado a um pagamento.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pagamento: {self.cliente.nome_completo}'


class RegistroPagamento(models.Model):
    data_pagamento = models.DateField(default=timezone.now)

    CHOICES_TIPO = [
        ("PIX", "Pix"),
        ("DEBITO", "Débito"),
        ("CREDITO", "Crédito"),
    ]
    tipo = models.CharField(max_length=8, choices=CHOICES_TIPO)
    total_pago = models.DecimalField(max_digits=10, decimal_places=2)
    pagamento = models.ForeignKey(
        Pagamento, on_delete=models.SET_NULL, null=True)
