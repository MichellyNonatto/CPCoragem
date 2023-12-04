from django.urls import path

from .views import (AdicionarPet, AdicionarServico, AdicionarTutor,
                    AdicionarVacinaPet, DeletarPet, DesvincularFuncionario,
                    DesvincularServico, EditarPet, EditarServico, ListaPets,
                    ListaServicos, ListaTurmas, PesquisarPet, PesquisarTutor,
                    VerPet, VerServicos, VerTurma, VincularServico,
                    VincularTutor)

app_name = 'servicos'

urlpatterns = [
    path('dashboard/pets', ListaPets.as_view(), name='listapets'),
    path('dashboard/pets/pesquisar', PesquisarPet.as_view(), name='pesquisarpet'),
    path('dashboard/pets/<int:pk>', VerPet.as_view(), name='verpet'),
    path('dashboard/pets/editarpet/<int:pk>',
         EditarPet.as_view(), name='editarpet'),
    path('dashboard/pets/deletarpet/<int:pk>',
         DeletarPet.as_view(), name='deletarpet'),
    path('dashboard/pets/adicionar_vacina/<int:pk>',
         AdicionarVacinaPet.as_view(), name='adicionarvacina'),

    path('dashboard/pets/vincular_tutor/adicionar_pet/<int:pk>',
         AdicionarPet.as_view(), name='adicionarpet'),
    path('dashboard/pets/vincular_tutor',
         VincularTutor.as_view(), name='vinculartutor'),
    path('dashboard/pets/vincular_tutor/pesquisar', PesquisarTutor.as_view(template_name='pets/vinculartutor.html'),
         name='pesquisartutor'),
    path('dashboard/pets/vincular_tutor/adicionar_tutor',
         AdicionarTutor.as_view(), name='adicionartutor'),

    path('dashboard/turmas', ListaTurmas.as_view(), name='listaturmas'),
    path('dashboard/turmas/<int:pk>', VerTurma.as_view(), name='verturma'),
    path('dashboard/turmas/desvincularservico/<int:servico_id>/<int:turma_id>', DesvincularServico.as_view(),
         name='desvincularservico'),
    path('dashboard/turmas/vincularservico/<int:pk>',
         VincularServico.as_view(), name='vincularservico'),

    path('dashboard/servicos', ListaServicos.as_view(), name='listaservicos'),
    path('dashboard/servicos/adicionar',
         AdicionarServico.as_view(), name='adicionarservico'),
    path('dashboard/servicos/<int:pk>',
         VerServicos.as_view(), name='verservicos'),
    path('dashboard/servicos/<int:servico_id>/<int:funcionario_id>', DesvincularFuncionario.as_view(),
         name='desvicularfuncionario'),
    path('dashboard/servicos/editarservico/<int:pk>',
         EditarServico.as_view(), name='editarservico'),

]
