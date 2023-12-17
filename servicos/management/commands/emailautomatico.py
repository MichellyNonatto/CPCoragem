import locale
from datetime import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from servicos.models import Pet
from usuarios.models import Pagamento, Usuario


class Command(BaseCommand):
    help = 'Envia e-mail com observações para tutores'

    def handle(self, *args, **options):
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        hoje = datetime.now().date()
        pagamentos = Pagamento.objects.exclude(registropagamento__isnull=False)

        clientes = Usuario.objects.filter(categoria='TUTOR').exclude(pagamento__registropagamento__isnull=False)

        for cliente in clientes:
            pets = Pet.objects.filter(tutor=cliente)
            servicos = []
            for pet in pets:
                valor_servico = {'nome': pet.nome, 'valor': pet.turma.valor_total}
                servicos.append(valor_servico)

            if servicos:
                print(f'Enviado para: {cliente.email}')
                pagamento = pagamentos.filter(cliente=cliente).first()
                self.enviar_email_pagamento(cliente.email, cliente.nome_completo, servicos,
                                            pagamento.total_pagamento, pagamento.dia_vencimento)

    def enviar_email_pagamento(self, destinatario, nome_cliente, servicos, valor_total, dia_vencimento):
        assunto = f"Aviso de Cobrança Automática - Pagamento referente ao mês de {dia_vencimento.strftime('%B')}"
        contexto = {
            'nome_cliente': nome_cliente,
            'servicos_realizados': servicos,
            'valor_total': valor_total,
            'data_validade': dia_vencimento.strftime('%B'),
        }
        html_message = render_to_string('email_mensagem/emailcobranca.html', contexto)
        texto_sem_formatacao = strip_tags(html_message)

        send_mail(
            assunto,
            texto_sem_formatacao,
            'crechepet.coragem@gmail.com',
            [destinatario],
            html_message=html_message,
        )
        self.stdout.write(self.style.SUCCESS('Comando executado com sucesso!'))
