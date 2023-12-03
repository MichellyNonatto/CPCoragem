from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView, DeleteView

from usuarios.forms import CriarTutorForm
from usuarios.models import Usuario, Pagamento, Funcionario
from .models import Pet, Vacinacao, Servico, Turma


class ListaPets(LoginRequiredMixin, ListView):
    template_name = 'pets/listapets.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_pk'] = self.request.user.pk
        return context


class PesquisarPet(LoginRequiredMixin, ListView):
    template_name = 'pets/listapets.html'
    model = Pet

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")
        if not termo_pesquisa or termo_pesquisa.isspace():
            return Pet.objects.none()

        resultados_pets = Pet.objects.filter(
            Q(nome__icontains=termo_pesquisa) |
            Q(raca__nome__icontains=termo_pesquisa) |
            Q(tutor__first_name__icontains=termo_pesquisa)
        )

        return resultados_pets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_pk'] = self.request.user.pk
        context['termo_pesquisa'] = self.request.GET.get("query")
        return context


class VerPet(LoginRequiredMixin, DetailView):
    template_name = 'pets/verpet.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.object

        vacinacoes = Vacinacao.objects.filter(pet=pet)

        context['vacinacoes'] = vacinacoes
        return context


class AdicionarVacinaPet(LoginRequiredMixin, CreateView):
    template_name = 'turmas/templates/pets/adicionarvacina.html'
    model = Vacinacao
    fields = ['vacina', 'data_vacinacao']

    def form_valid(self, form):
        try:
            pet = Pet.objects.get(pk=self.kwargs['pk'])
        except Pet.DoesNotExist:
            return redirect('error_page')

        vacinacao = form.save(commit=False)
        vacinacao.pet = pet
        vacinacao.save()
        success_url = reverse('servicos:verpet',
                              kwargs={'pk': vacinacao.pet.pk}) + '?mensagem=Vacina vinculada com sucesso!'
        return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = self.kwargs['pk']
        return context


class VincularTutor(LoginRequiredMixin, ListView):
    template_name = 'pets/vinculartutor.html'
    model = Usuario


class AdicionarPet(LoginRequiredMixin, CreateView):
    template_name = 'pets/adicionarpet.html'
    model = Pet
    fields = ['imagem', 'nome', 'data_nascimento', 'genero', 'raca', 'descricao_medica', 'castrado', 'turma']

    def form_valid(self, form):
        try:
            tutor = Usuario.objects.get(pk=self.kwargs['pk'])
        except Usuario.DoesNotExist:
            return redirect('error_page')

        pet = form.save(commit=False)
        pet.tutor = tutor
        pet.save()
        success_url = reverse('servicos:listapets') + '?mensagem=Pet adicionado com sucesso!'
        return redirect(success_url)


class PesquisarTutor(LoginRequiredMixin, ListView):
    model = Usuario

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")
        if not termo_pesquisa or termo_pesquisa.isspace():
            return Usuario.objects.none()

        resultados_tutores = Usuario.objects.filter(
            Q(nome_completo__icontains=termo_pesquisa) |
            Q(documento__icontains=termo_pesquisa) |
            Q(endereco__cidade__icontains=termo_pesquisa) |
            Q(endereco__cep__icontains=termo_pesquisa) |
            Q(email__icontains=termo_pesquisa) |
            Q(telefone__icontains=termo_pesquisa)

        )
        return resultados_tutores

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        titulo = 'Vincular Tutor'

        context['titulo'] = titulo
        context['usuario_pk'] = self.request.user.pk
        context['termo_pesquisa'] = self.request.GET.get("query")
        context['usuario_atual'] = self.request.user
        return context


class AdicionarTutor(LoginRequiredMixin, FormView):
    template_name = 'pets/adicionartutor.html'
    form_class = CriarTutorForm

    def form_valid(self, form):
        documento = form.cleaned_data['documento']

        if Usuario.objects.filter(documento=documento).exists():
            messages.error(self.request, 'Tutor já existe em nossa base de dados.')
        else:
            form.save()
            success_url = reverse('servicos:vinculartutor') + '?mensagem=Tutor adicionado com sucesso!'
            return redirect(success_url)

        return reverse('servicos:listapets')


class ListaTurmas(LoginRequiredMixin, ListView):
    template_name = 'turmas/listaturmas.html'
    model = Turma


class VerTurma(LoginRequiredMixin, DetailView):
    template_name = 'turmas/verturma.html'
    model = Turma

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        turma = Turma.objects.get(id=self.kwargs['pk'])
        pets = Pet.objects.filter(turma=turma)
        context['pets'] = pets
        return context


class DesvincularServico(LoginRequiredMixin, View):
    template_name = 'turmas/verturma.html'

    def desvincular_servico(self, request, servico_id, turma_id):
        servico = get_object_or_404(Servico, id=servico_id)
        turma = get_object_or_404(Turma, id=turma_id)
        turma.servicos.remove(servico)
        turma.save()
        messages.success(request, 'Serviço desvinculado da turma com sucesso!')

        return HttpResponseRedirect(reverse('servicos:verturma', args=[turma.pk]))

    def get(self, request, servico_id, turma_id):
        return self.desvincular_servico(request, servico_id, turma_id)


class ListaServicos(LoginRequiredMixin, ListView):
    model = Servico
    template_name = 'listaservicos.html'


class VincularServico(LoginRequiredMixin, ListView):
    model = Servico
    template_name = 'turmas/vincularservico.html'
    context_object_name = 'servicos_todos'

    def vincular_servico(self, request, servico_id, pk):
        turma = get_object_or_404(Turma, id=pk)
        servico = get_object_or_404(Servico, id=servico_id)
        turma.servicos.add(servico)
        turma.save()
        messages.success(request, 'Serviço vinculado à turma com sucesso!')
        return HttpResponseRedirect(reverse('servicos:verturma', args=[turma.pk]))

    def get(self, request, pk):
        return super().get(request, pk)

    def post(self, request, pk):
        servico_id = request.POST.get('servico_id')
        return self.vincular_servico(request, servico_id, pk)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        turma = Turma.objects.get(id=self.kwargs['pk'])
        servicos_nao_vinculados = Servico.objects.exclude(id__in=[servico.id for servico in turma.servicos.all()])
        context['servicos_nao_vinculados'] = servicos_nao_vinculados
        return context