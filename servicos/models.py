from django.db import models
from django.utils import timezone

from usuarios.models import Funcionario, Usuario


#   Caso seja a primeira vez que executa o migration utilize o command  ``python manage.py diaDaSemana``
class DiaDaSemana(models.Model):
    dia = models.CharField(max_length=4)

    @staticmethod
    def create_dias_da_semana():
        dias_da_semana = ['Seg', 'Ter', 'Quar', 'Quin', 'Sex']
        for dia in dias_da_semana:
            DiaDaSemana.objects.get_or_create(dia=dia)

    def __str__(self):
        return self.dia


class Servico(models.Model):
    nome = models.CharField(max_length=45)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dias_da_semana = models.ManyToManyField(DiaDaSemana)
    funcionarios = models.ManyToManyField(
        Funcionario, limit_choices_to=~models.Q(funcao__descricao__iexact='Gerente'))

    def __str__(self):
        return self.nome

    def get_dias_da_semana_ids(self):
        return list(self.dias_da_semana.values_list('pk', flat=True))

    def get_valor_formatado(self):
        return str(self.valor).replace(',', '.')


class Turma(models.Model):
    nome = models.CharField(max_length=45)
    servicos = models.ManyToManyField(Servico)
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nome


class Raca(models.Model):
    nome = models.CharField(max_length=45)

    CHOICES_ESPECIE = [
        ("CACHORRO", "Cachorro"),
        ("GATO", "Gato"),
    ]
    especie = models.CharField(max_length=45, choices=CHOICES_ESPECIE)

    def __str__(self):
        return f"{self.nome} - {self.get_especie_display()}"


class Pet(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to='imagens_pet/')
    nome = models.CharField(max_length=45)
    data_nascimento = models.DateField()

    CHOICES_GENERO = [
        ("FEMININO", "Feminino"),
        ("MASCULINO", "Masculino"),
    ]
    genero = models.CharField(max_length=45, choices=CHOICES_GENERO)
    castrado = models.BooleanField(
        help_text='Marque esta caixa se o animal for castrado.', default=False)
    descricao_medica = models.TextField(
        max_length=200, default="Nenhum tipo de observação.")

    tutor = models.ForeignKey(
        Usuario, related_name="tutor", on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, related_name="raca",
                             on_delete=models.DO_NOTHING)
    turma = models.ForeignKey(
        Turma, related_name='turma', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    nome = models.CharField(max_length=45)
    dose = models.SmallIntegerField()  # 0 até 32767
    idade_minima_em_meses = models.SmallIntegerField(blank=True)
    tempo_de_espera_em_dias = models.SmallIntegerField()

    def __str__(self):
        return self.nome


class Vacinacao(models.Model):
    vacina = models.ManyToManyField(Vacina)
    pet = models.ForeignKey(Pet, related_name="pets", on_delete=models.CASCADE)

    def __str__(self):
        informacao = f"Pet: {self.pet}"
        return informacao
