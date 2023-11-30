from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from servicos.models import Turma
from usuarios.models import Pagamento, Usuario


@receiver(post_save, sender=Turma)
def atualizar_total_pagamento(sender, instance, **kwargs):
    tutor = instance.pet.tutor

    if isinstance(tutor, Usuario) and tutor.categoria == 'TUTOR':
        pagamento_tutor = Pagamento.objects.filter(cliente=tutor).order_by('-id').first()

        if pagamento_tutor:
            grade = Turma.objects.get(pet__tutor=pagamento_tutor.cliente)
            total_pagamento = grade.servico.valor
            pagamento_tutor.total_pagamento = total_pagamento
            pagamento_tutor.save()
