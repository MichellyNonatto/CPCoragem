from django.db.models.signals import post_save
from django.dispatch import receiver

from servicos.models import Pet
from usuarios.models import Pagamento


@receiver(post_save, sender=Pet)
def atualizar_pagamento_tutor(sender, instance, **kwargs):
    tutor = instance.tutor
    pagamento = Pagamento.objects.filter(cliente=tutor).order_by('-id').first()
    turma = instance.turma
    pagamento.total_pagamento = turma.valor_total
    pagamento.save()