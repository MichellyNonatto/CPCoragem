from django.core.management.base import BaseCommand
from servicos.models import DiaDaSemana


class Command(BaseCommand):
    help = 'Cria os valores pré-determinados para DiaDaSemana'

    def handle(self, *args, **options):
        DiaDaSemana.create_dias_da_semana()
        self.stdout.write(self.style.SUCCESS('Valores pré-determinados para DiaDaSemana foram criados com sucesso.'))
