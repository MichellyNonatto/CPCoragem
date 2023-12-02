from django.urls import path
from django.contrib.auth import views as auth_view

from .views import CustomLoginView, Dashboard, EditarPerfilUsuario, EditarPerfilEndereco, RecuperarConta, Autenticacao, \
    AtualizarSenha, ListaFuncionarios, PesquisaFuncionarios, VerFuncionario, EditarFuncionario, DeletarFuncionario, \
    AdicionarFuncionario, AutenticacaoClienteView, CriarNovoPagamento, ListaPagamentos, PesquisarPagamento, \
    DeletarCliente

app_name = 'usuarios'

urlpatterns = [
    path('', CustomLoginView.as_view(template_name='desconnect/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='desconnect/logout.html'), name='logout'),

    path('dashboard/<int:pk>', Dashboard.as_view(), name='dashboard'),
    path('editarperfil/<int:pk>/', EditarPerfilUsuario.as_view(), name='editarperfil'),
    path('editarperfil/editar_endereco/<int:pk>', EditarPerfilEndereco.as_view(), name='editarendereco'),

    path('recuperar_conta/', RecuperarConta.as_view(), name='recuperarconta'),
    path('recuperacao_de_conta/autenticacao/<int:pk>', Autenticacao.as_view(), name='autenticacao'),
    path('recuperacao_de_conta/autenticacao/atualizarsenha/<int:pk>', AtualizarSenha.as_view(), name='atualizarsenha'),

    path('dashboard/funcionarios', ListaFuncionarios.as_view(), name='listafuncionarios'),
    path('dashboard/funcionarios/pesquisa', PesquisaFuncionarios.as_view(), name='pesquisafuncionarios'),
    path('dashboard/funcionarios/<int:pk>', VerFuncionario.as_view(), name='verfuncionario'),
    path('dashboard/funcionarios/editar_funcionario/<int:pk>', EditarFuncionario.as_view(), name='editarfuncionario'),
    path('dashboard/funcionarios/deletar_funcionario/<int:pk>', DeletarFuncionario.as_view(),
         name='deletarfuncionario'),
    path('dashboard/funcionarios/adicionar_funcionario', AdicionarFuncionario.as_view(), name='adicionarfuncionario'),

    path('dashboard/financeiro/', ListaPagamentos.as_view(), name='financeiro'),
    path('dashboard/financeiro/pesquisa', PesquisarPagamento.as_view(template_name='funcionario/listapagamento.html'),
         name='pesquisarfinanceiro'),
    path('dashboard/financeiro/<int:pk>', DeletarCliente.as_view(), name='deletarcliente'),

    path('cliente_coragem/verificacao', AutenticacaoClienteView.as_view(), name='autenticacaocliente'),
    path('cliente_coragem/pagamento/<int:pk>', CriarNovoPagamento.as_view(), name='atualizarpagamento'),
]
