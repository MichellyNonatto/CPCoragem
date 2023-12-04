from django.urls import resolve

from .models import Funcionario


def funcionario(request):
    funcionario_context = None
    urls_context = None

    if request.user.is_authenticated:
        try:
            funcionario = Funcionario.objects.get(usuario=request.user)
            funcionario_context = funcionario

            if funcionario.funcao == 'Gerente':
                urls = {
                    'Dashboard': 'usuarios:dashboard',
                    'Funcionários': 'usuarios:funcionarios',
                    'Financeiro': 'usuarios:financeiro',
                }
                urls_context = urls.items()
            else:
                urls = {
                    'Dashboard': 'usuarios:dashboard',
                    'Pets': 'servicos:pets',
                    'Serviços': 'servicos:servicos',
                    'Turmas': 'servicos:turmas',
                }
                urls_context = urls.items()

                resolver_match = resolve(request.path_info)
                url_name = resolver_match.route

                url_parent = None
                if '/' in url_name:
                    parts = url_name.split('/')
                    url_parent = parts[0]

        except Funcionario.DoesNotExist:
            pass

    return {'funcionario_context': funcionario_context, 'urls_context': urls_context, 'url_pai': url_parent}
