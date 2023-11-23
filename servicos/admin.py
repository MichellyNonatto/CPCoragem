from django.contrib import admin

from .models import Servico, Pet, Raca, Vacina, Vacinacao, Grade

# Register your models here.
admin.site.register(Servico)
admin.site.register(Pet)
admin.site.register(Raca)
admin.site.register(Vacina)
admin.site.register(Vacinacao)
admin.site.register(Grade)