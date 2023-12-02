from .models import Funcionario


def funcionario(request):
    if request.user.is_authenticated:
        try:
            funcionario = Funcionario.objects.get(usuario=request.user)
        except Funcionario.DoesNotExist:
            funcionario = None
    else:
        funcionario = None

    return {'funcionario_context': funcionario}
