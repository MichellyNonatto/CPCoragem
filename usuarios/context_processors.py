from django.urls import resolve

from .models import Funcionario

def funcionario(request):
    funcionario_context = None
    urls_context = None
    url_parent = None

    if request.user.is_authenticated:
        try:
            funcionario = Funcionario.objects.get(usuario=request.user)

            if funcionario:
                funcionario_context = funcionario

            if funcionario.funcao.descricao == 'Gerente':
                urls = {
                    'Dashboard': 'usuarios:dashboard',
                    'Funcionarios': 'usuarios:funcionarios',
                    'Financeiro': 'usuarios:financeiro',
                    'Clientes': 'usuarios:listatutor'
                }
                urls_context = urls.items()
            else:
                urls = {
                    'Dashboard': 'usuarios:dashboard',
                    'Pets': 'servicos:pets',
                    'Servicos': 'servicos:servicos',
                    'Turmas': 'servicos:turmas',
                    'Clientes': 'usuarios:listatutor'
                }
                urls_context = urls.items()

            resolver_match = resolve(request.path_info)
            url_name = resolver_match.route

            if '/' in url_name:
                parts = url_name.split('/')
                url_parent = parts[0]

        except Funcionario.DoesNotExist:
            pass

    return {'funcionario_context': funcionario_context, 'urls_context': urls_context, 'url_pai': url_parent}

