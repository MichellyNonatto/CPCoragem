from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from servicos.models import Servico, Turma


@receiver(m2m_changed, sender=Turma.servicos.through)
def atualizar_pagamento_turma(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        servicos = instance.servicos.all()
        valor_total = sum(servico.valor for servico in servicos)
        instance.valor_total = valor_total
        instance.save()


@receiver(post_save, sender=Servico)
def atualizar_pagamento_servico(sender, instance, **kwargs):
    turmas = Turma.objects.filter(servicos__id=instance.id)

    for turma in turmas:
        servicos_na_turma = turma.servicos.all()
        turma.valor_total = sum(servico.valor for servico in servicos_na_turma)
        turma.save()
