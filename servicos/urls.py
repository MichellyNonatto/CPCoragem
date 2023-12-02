from django.urls import path

from .views import ListaPets, PesquisarPet, VerPet, AdicionarVacinaPet, AdicionarPet, \
    VincularTutor, PesquisarTutor, AdicionarTutor, ListaTurmas, AdicionarPetServico, DeletarPetServico, VerTurma

app_name = 'servicos'

urlpatterns = [
    path('dashboard/pets', ListaPets.as_view(), name='listapets'),
    path('dashboard/pets/pesquisar', PesquisarPet.as_view(), name='pesquisarpet'),
    path('dashboard/pets/<int:pk>', VerPet.as_view(), name='verpet'),
    path('dashboard/pets/adicionar_vacina/<int:pk>', AdicionarVacinaPet.as_view(), name='adicionarvacina'),

    path('dashboard/pets/vincular_tutor/adicionar_pet/<int:pk>', AdicionarPet.as_view(), name='adicionarpet'),
    path('dashboard/pets/vincular_tutor', VincularTutor.as_view(), name='vinculartutor'),
    path('dashboard/pets/vincular_tutor/pesquisar', PesquisarTutor.as_view(template_name='pets/vinculartutor.html'), name='pesquisartutor'),
    path('dashboard/pets/vincular_tutor/adicionar_tutor', AdicionarTutor.as_view(), name='adicionartutor'),

    path('dashboard/turmas', ListaTurmas.as_view(), name='listaturmas'),
    path('dashboard/turmas/<int:pk>', VerTurma.as_view(), name='verturma'),
    path('dashboard/turmas/adicionar_servico/<int:pk>', AdicionarPetServico.as_view(), name='adicionarservico'),
    path('dashboard/turmas/deletar_servico/<int:servico_pk>/<int:pk>', DeletarPetServico.as_view(), name='deletarservico'),
]
