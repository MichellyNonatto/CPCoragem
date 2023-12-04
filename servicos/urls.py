from django.urls import path

from .views import (AdicionarPet, AdicionarServico, AdicionarTutor,
                    AdicionarVacinaPet, DeletarPet, DesvincularFuncionario,
                    DesvincularServico, EditarPet, EditarServico, ListaPets,
                    ListaServicos, ListaTurmas, PesquisarPet, PesquisarServico,
                    PesquisarTurma, PesquisarTutor, VerPet, VerServicos,
                    VerTurma, VincularTutor, EditarTurma)

app_name = 'servicos'

urlpatterns = [
    path('pets', ListaPets.as_view(), name='pets'),
    path('pets/pesquisar', PesquisarPet.as_view(), name='pesquisarpet'),
    path('pets/<int:pk>', VerPet.as_view(), name='verpet'),
    path('pets/editarpet/<int:pk>', EditarPet.as_view(), name='editarpet'),
    path('pets/deletarpet/<int:pk>', DeletarPet.as_view(), name='deletarpet'),
    path('pets/adicionar_vacina/<int:pk>', AdicionarVacinaPet.as_view(), name='adicionarvacina'),
    path('pets/vincular_tutor/adicionar_pet/<int:pk>',AdicionarPet.as_view(), name='adicionarpet'),
    path('pets/vincular_tutor', VincularTutor.as_view(), name='vinculartutor'),
    path('pets/vincular_tutor/pesquisar', PesquisarTutor.as_view(template_name='pets/vinculartutor.html'),name='pesquisartutor'),
    path('pets/vincular_tutor/adicionar_tutor', AdicionarTutor.as_view(), name='adicionartutor'),

    path('turmas', ListaTurmas.as_view(), name='turmas'),
    path('turmas/pesquisar', PesquisarTurma.as_view(), name='pesquisarturma'),
    path('turmas/<int:pk>', VerTurma.as_view(), name='verturma'),
    path('turmas/editarservico/<int:pk>', EditarTurma.as_view(),name='editarturma'),
    path('turmas/desvincularservico/<int:servico_id>/<int:turma_id>', DesvincularServico.as_view(), name='desvincularservico'),

    path('servicos', ListaServicos.as_view(), name='servicos'),
    path('servicos/pesquisar', PesquisarServico.as_view(), name='pesquisarservico'),
    path('servicos/adicionar', AdicionarServico.as_view(), name='adicionarservico'),
    path('servicos/<int:pk>', VerServicos.as_view(), name='verservicos'),
    path('servicos/<int:servico_id>/<int:funcionario_id>', DesvincularFuncionario.as_view(), name='desvicularfuncionario'),
    path('servicos/editarservico/<int:pk>', EditarServico.as_view(), name='editarservico'),
]
