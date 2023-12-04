from django.urls import path

from .views import ListaPets, PesquisarPet, VerPet, AdicionarVacinaPet, AdicionarPet, \
    VincularTutor, PesquisarTutor, AdicionarTutor, ListaTurmas, VerTurma, DesvincularServico, VincularServico, \
    ListaServicos, VerServicos, DesvincularFuncionario, VincularFuncionario, EditarPet, DeletarPet

app_name = 'servicos'

urlpatterns = [
    path('pets', ListaPets.as_view(), name='pets'),
    path('pets/pesquisar', PesquisarPet.as_view(), name='pesquisarpet'),
    path('pets/<int:pk>', VerPet.as_view(), name='verpet'),
    path('pets/editarpet/<int:pk>', EditarPet.as_view(), name='editarpet'),
    path('pets/deletarpet/<int:pk>', DeletarPet.as_view(), name='deletarpet'),
    path('pets/adicionar_vacina/<int:pk>', AdicionarVacinaPet.as_view(), name='adicionarvacina'),

    path('pets/vincular_tutor/adicionar_pet/<int:pk>', AdicionarPet.as_view(), name='adicionarpet'),
    path('pets/vincular_tutor', VincularTutor.as_view(), name='vinculartutor'),
    path('pets/vincular_tutor/pesquisar', PesquisarTutor.as_view(template_name='pets/vinculartutor.html'),
         name='pesquisartutor'),
    path('pets/vincular_tutor/adicionar_tutor', AdicionarTutor.as_view(), name='adicionartutor'),

    path('turmas', ListaTurmas.as_view(), name='turmas'),
    path('turmas/<int:pk>', VerTurma.as_view(), name='verturma'),
    path('turmas/desvincularservico/<int:servico_id>/<int:turma_id>', DesvincularServico.as_view(),
         name='desvincularservico'),
    path('turmas/vincularservico/<int:pk>', VincularServico.as_view(), name='vincularservico'),

    path('servicos', ListaServicos.as_view(), name='servicos'),
    path('servicos/<int:pk>', VerServicos.as_view(), name='verservicos'),
    path('servicos/<int:servico_id>/<int:funcionario_id>', DesvincularFuncionario.as_view(),
         name='desvicularfuncionario'),
    path('servicos/vincularfuncionario/<int:pk>', VincularFuncionario.as_view(), name='vincularfuncionario'),

]
