from datetime import datetime, time, date
from django.shortcuts import render
from django.urls import reverse, resolve
import holidays
from usuarios.models import Funcionario


class Funcionamento:
    def __init__(self):
        self._inicio = time(8, 30)
        self._fim = time(18, 00)

    def get_funcionamento(self):
        br_holiday = holidays.country_holidays('BR')
        feriado = date(datetime.now().year, datetime.now().month, datetime.now().day) in br_holiday
        hora = datetime.now().time()
        semana = datetime.now().weekday()

        return self._inicio <= hora <= self._fim and semana <= 4 and not feriado

    @staticmethod
    def mensagem(now=None):
        if now is None:
            now = datetime.now().time()

        if time(5, 0) <= now <= time(12, 0):
            return "Bom dia"
        elif time(12, 0) < now <= time(19, 0):
            return "Boa tarde"
        else:
            return "Boa noite"


class FuncionamentoMiddleware:
    def __init__(self, get_response):
        self.request = None
        self.get_response = get_response

    def __call__(self, request):
        funcionamento = Funcionamento()
        if not funcionamento.get_funcionamento():
            return render(self.request, 'error/error_504.html')

        response = self.get_response(request)
        return response


class Acesso:
    def get_acesso_conta(self, user):
        if user.email.endswith("@coragem.com.br"):
            if user.categoria == "FUNCIONARIO":
                return True
        return False


class Urls:
    def get_acesso_urls(self, user, url, app):
        if user.is_authenticated:
            try:
                funcionario = Funcionario.objects.get(usuario__email=user)
            except:
                return True
            allowed_urls = [
                reverse('usuarios:verfuncionario', kwargs={'pk': funcionario.pk}),
                reverse('usuarios:editarfuncionario', kwargs={'pk': funcionario.pk}),
                reverse('usuarios:deletarfuncionario', kwargs={'pk': funcionario.pk}),
                reverse('usuarios:adicionarfuncionario'),
                reverse('usuarios:pesquisafuncionarios'),
                reverse('usuarios:listafuncionarios'),
            ]

            if url in allowed_urls and funcionario.funcao.descricao != "Gerente":
                if 'servicos' in app:
                    return False
                return False
        return True


class UrlsMiddleware:
    def __init__(self, get_response):
        self.request = None
        self.get_response = get_response

    def __call__(self, request):
        acesso = Urls()
        if not acesso.get_acesso_urls(request.user, request.path, resolve(request.path_info).app_name):
            return render(self.request, 'error/error_403.html')

        response = self.get_response(request)
        return response
