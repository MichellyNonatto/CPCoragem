from django.db import models
from django.utils import timezone

from usuarios.models import Funcionario, Usuario


#   Caso seja a primeira vez que executa o migration utilize o command  ``python manage.py diaDaSemana``
class DiaDaSemana(models.Model):
    dia = models.CharField(max_length=20)

    @staticmethod
    def create_dias_da_semana():
        dias_da_semana = ['Segunda-feira', 'Terça-feira',
                          'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
        for dia in dias_da_semana:
            DiaDaSemana.objects.get_or_create(dia=dia)

    def __str__(self):
        return self.dia


class Servico(models.Model):
    nome = models.CharField(max_length=45)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dias_da_semana = models.ManyToManyField(DiaDaSemana)
    funcionarios = models.ManyToManyField(Funcionario)

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
        return self.nome


class Pet(models.Model):
    imagem = models.ImageField(upload_to='imagens_pet/')
    nome = models.CharField(max_length=45)
    data_nascimento = models.DateField()

    CHOICES_GENERO = [
        ("FEMININO", "Feminino"),
        ("MASCULINO", "Masculino"),
    ]
    genero = models.CharField(max_length=45, choices=CHOICES_GENERO)

    tutor = models.ForeignKey(
        Usuario, related_name="tutor", on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, related_name="raca",
                             on_delete=models.DO_NOTHING)
    descricao_medica = models.TextField(
        max_length=200, default="Nenhum tipo de observação.")
    castrado = models.BooleanField(
        help_text='Marque esta caixa se o animal for castrado.', default=False)

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    nome = models.CharField(max_length=45)
    dose = models.SmallIntegerField()  # 0 até 32767
    idade_minima_em_semanas = models.SmallIntegerField(blank=True)
    tempo_de_espera_em_dias = models.SmallIntegerField()

    def __str__(self):
        return self.nome


class Vacinacao(models.Model):
    vacina = models.ForeignKey(
        Vacina, related_name="vacinacao", on_delete=models.DO_NOTHING)
    pet = models.ForeignKey(Pet, related_name="pet", on_delete=models.CASCADE)
    data_vacinacao = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.vacina.nome)


class Grade(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    ultima_visita = models.DateField(default=timezone.now)
    observacao = models.TextField(
        max_length=250, default="Nenhum tipo de observação.")

    class Meta:
        unique_together = ['pet', 'servico']

    def __str__(self):
        informacao = f"{self.pet.nome} {self.servico.nome}"
        return informacao
