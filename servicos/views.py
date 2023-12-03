from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from usuarios.forms import CriarTutorForm
from usuarios.models import Funcionario, Pagamento, Usuario

from .models import Pet, Servico, Turma, Vacinacao


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

        vacinacoes = Vacinacao.objects.filter(pet=pet).select_related('vacina')
        list_vacina = vacinacoes.values_list('vacina__nome', flat=True)

        context['vacinacoes'] = ','.join(list_vacina)
        return context


class EditarPet(LoginRequiredMixin, UpdateView):
    template_name = 'pets/editarpet.html'
    model = Pet
    fields = ['imagem', 'nome', 'data_nascimento', 'genero',
              'raca', 'descricao_medica', 'castrado', 'turma']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_tutor'] = self.object.tutor.nome_completo
        return context

    def get_success_url(self):
        messages.success(self.request, 'Pet editado com sucesso!')
        return reverse('servicos:verpet', args=[self.object.pk])


class DeletarPet(LoginRequiredMixin, DeleteView):
    template_name = 'containers/deletar.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_deletar'] = self.object.nome
        return context

    def get_success_url(self):
        messages.success(self.request, 'Pet deletado com sucesso!')
        return reverse('servicos:listapets')


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
    fields = ['imagem', 'nome', 'data_nascimento', 'genero',
              'raca', 'descricao_medica', 'castrado', 'turma']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            tutor = Usuario.objects.get(pk=self.kwargs['pk'])
            context['nome_tutor'] = tutor.nome_completo
        except Usuario.DoesNotExist:
            context['nome_tutor'] = None

        return context

    def form_valid(self, form):
        try:
            tutor = Usuario.objects.get(pk=self.kwargs['pk'])
        except Usuario.DoesNotExist:
            return redirect('error_page')

        pet = form.save(commit=False)
        pet.tutor = tutor
        pet.save()
        success_url = reverse('servicos:listapets') + \
            '?mensagem=Pet adicionado com sucesso!'
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
            messages.error(
                self.request, 'Tutor já existe em nossa base de dados.')
        else:
            form.save()
            success_url = reverse('servicos:vinculartutor') + \
                '?mensagem=Tutor adicionado com sucesso!'
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
    template_name = 'servicos/listaservicos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servico_ids'] = [list(servico.dias_da_semana.values_list(
            'id', flat=True)) for servico in context['object_list']]
        return context


class VincularServico(LoginRequiredMixin, UpdateView):
    model = Turma
    template_name = 'turmas/vincularservico.html'
    fields = ["servicos"]

    def get_success_url(self):
        messages.success(
            self.request, 'Serviço vinculado há turma com sucesso!')
        return reverse('servicos:verturma', args=[self.object.pk])


class PesquisarServico(LoginRequiredMixin, ListView):
    template_name = 'servicos/listaservicos.html'
    model = Servico

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get("query")
        if not termo_pesquisa or termo_pesquisa.isspace():
            return Servico.objects.none()

        resultados_servicos = Servico.objects.filter(
            Q(nome__icontains=termo_pesquisa)
        )
        return resultados_servicos

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servico_ids'] = [list(servico.dias_da_semana.values_list(
            'id', flat=True)) for servico in context['object_list']]
        context['termo_pesquisa'] = self.request.GET.get("query")
        return context


class VerServicos(LoginRequiredMixin, DetailView):
    template_name = 'servicos/verservico.html'
    model = Servico


class DesvincularFuncionario(LoginRequiredMixin, View):
    template_name = 'servicos/verservico.html'

    def desvincular_funcionario(self, request, servico_id, funcionario_id):
        servico = get_object_or_404(Servico, id=servico_id)
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        servico.funcionarios.remove(funcionario)
        servico.save()
        messages.success(
            request, 'Funcionário desvinculado do serviço com sucesso!')

        return HttpResponseRedirect(reverse('servicos:verservicos', args=[servico.pk]))

    def get(self, request, servico_id, funcionario_id):
        return self.desvincular_funcionario(request, servico_id, funcionario_id)


class VincularFuncionario(LoginRequiredMixin, UpdateView):
    model = Servico
    template_name = 'servicos/vincularfuncionario.html'
    fields = ["funcionarios"]

    def get_success_url(self):
        messages.success(
            self.request, 'Funcionário vinculado ao serviço com sucesso!')
        return reverse('servicos:verservicos', args=[self.object.pk])
