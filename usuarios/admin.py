from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Endereco, Usuario, Funcao, Funcionario, Pagamento, RegistroPagamento

# Register your models here.
campo = list(UserAdmin.fieldsets)
campo.append(
    ("Informações", {'fields': ('nome_completo', 'telefone', 'documento', 'categoria', 'endereco')})
)

UserAdmin.fieldsets = tuple(campo)
admin.site.register(Endereco)

admin.site.register(Usuario, UserAdmin)

admin.site.register(Funcionario)
admin.site.register(Funcao)

admin.site.register(Pagamento)
admin.site.register(RegistroPagamento)