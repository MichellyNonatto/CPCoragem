import locale

from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.html import strip_tags
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from servicos.models import Grade, Pet
from usuarios.models import Usuario, Pagamento


class Command(BaseCommand):
    help = 'Envia e-mail com observações para tutores'

    def handle(self, *args, **kwargs):
        if timezone.now().day == 1:
            self.enviar_observacoes()

        self.enviar_pagamento()

    def enviar_observacoes(self):
        tutores = Usuario.objects.filter(categoria='TUTOR')

        for tutor in tutores:
            pets_tutor = Pet.objects.filter(tutor=tutor)
            observacoes = []

            for pet in pets_tutor:
                grades_pet = Grade.objects.filter(pet=pet)
                for grade in grades_pet:
                    servico = [grade.servico.nome, grade.observacao]
                    observacoes.append(servico)

            if observacoes:
                self.enviar_email_obeservacao(tutor.email, tutor.nome_completo, observacoes)

    def enviar_email_obeservacao(self, destinatario, nome_tutor, observacoes):
        assunto = 'Observações dos Serviços Prestados aos Pets'
        contexto = {'nome_tutor': nome_tutor, 'observacoes': observacoes}
        html_message = render_to_string('email_mensagem/emailobservacoes.html', contexto)
        texto_sem_formatacao = strip_tags(html_message)

        send_mail(
            assunto,
            texto_sem_formatacao,
            'crechePet_coragem@outlook.com',
            [destinatario],
            html_message=html_message,
        )

    def enviar_pagamento(self):
        global servicos
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        hoje = datetime.now().date()
        pagamentos = Pagamento.objects.all()

        pagamentos = pagamentos.exclude(registropagamento__isnull=False)

        clientes = Usuario.objects.filter(categoria='TUTOR')
        clientes = clientes.exclude(pagamento__registropagamento__isnull=False)

        for pagamento in pagamentos:
            if timedelta(days=-5) < (pagamento.dia_vencimento - hoje) <= timedelta(days=10):
                print(f'Contas não pagas: {pagamentos}')
                for cliente in clientes:
                    pets = Pet.objects.filter(tutor=cliente)
                    servicos = []
                    for pet in pets:
                        servico_valor = Grade.objects.filter(pet=pet)
                        for valor in servico_valor:
                            valor_servico = {'nome': valor.servico.nome, 'valor': valor.servico.valor}
                            servicos.append(valor_servico)
                if servicos:
                    print(f'Enviado para: {cliente.email}')
                    self.enviar_email_pagamento(cliente.email, cliente.nome_completo, servicos,
                                                pagamento.total_pagamento, pagamento.dia_vencimento)

    def enviar_email_pagamento(self, destinatario, nome_cliente, servicos, valor_total, dia_vencimento):
        assunto = 'Detalhes do Pagamento'
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
