from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from usuarios.forms import CriarTutorForm
from usuarios.models import Pagamento, Usuario

from .models import Grade, Pet, Servico, Vacinacao


class ListaPets(LoginRequiredMixin, ListView):
    template_name = 'listapets.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_pk'] = self.request.user.pk
        return context


class PesquisarPet(LoginRequiredMixin, ListView):
    template_name = 'listapets.html'
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
    template_name = 'verpet.html'
    model = Pet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.object

        vacinacoes = Vacinacao.objects.filter(pet=pet)

        nomes_vacinas = ", ".join(list(Vacinacao.objects.filter(
            pet=pet).values_list('vacina__nome', flat=True)))

        print("Nomes de Vacinas:", nomes_vacinas)

        context['nomes_vacinas'] = nomes_vacinas

        context['vacinacoes'] = vacinacoes
        return context


class AdicionarVacinaPet(LoginRequiredMixin, CreateView):
    template_name = 'adicionarvacina.html'
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
        context['pet'] = self.kwargs['pk']
        return context


class VincularTutor(LoginRequiredMixin, ListView):
    template_name = 'vinculartutor.html'
    model = Usuario


class AdicionarPet(LoginRequiredMixin, CreateView):
    template_name = 'adicionarpet.html'
    model = Pet
    fields = ['imagem', 'nome', 'data_nascimento',
              'genero', 'raca', 'descricao_medica', 'castrado']

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
    template_name = 'adicionartutor.html'
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


class ListaServicos(LoginRequiredMixin, ListView):
    model = Servico
    template_name = 'listaservicos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_pk'] = self.request.user.pk
        context['servico_ids'] = [list(servico.dias_da_semana.values_list(
            'id', flat=True)) for servico in context['object_list']]

        return context


class PesquisarServico(LoginRequiredMixin, ListView):
    template_name = 'listaservicos.html'
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
        context['usuario_pk'] = self.request.user.pk
        context['termo_pesquisa'] = self.request.GET.get("query")
        return context


class VerServicos(LoginRequiredMixin, DetailView):
    template_name = 'verservico.html'
    model = Servico

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets_cadastrado = Grade.objects.filter(servico=self.kwargs['pk'])
        context['pets_cadastrado'] = pets_cadastrado
        return context


class EditarGrade(LoginRequiredMixin, UpdateView):
    template_name = 'editargrade.html'
    model = Grade
    fields = ['observacao']

    def form_valid(self, form):
        grade = Grade.objects.get(pk=self.kwargs['pk'])
        servico = Servico.objects.get(pk=grade.servico.pk)
        dias_da_semana = servico.dias_da_semana.values()
        dias_list = []

        for dia in dias_da_semana:
            dias_list.append(dia['id'])

        if timezone.now().date() != form.instance.ultima_visita and form.instance.ultima_visita.isoweekday() not in dias_da_semana:
            form.instance.ultima_visita = timezone.now()
            pagamento = Pagamento.objects.filter(
                cliente=grade.pet.tutor).order_by('-dia_vencimento').first()
            pagamento.total_pagamento += servico.valor
            pagamento.save()
            success_url = reverse('servicos:verservicos', kwargs={
                                  'pk': grade.servico.pk})
            return redirect(success_url)
        else:
            messages.error(self.request, 'A atualização do pet já foi feita!')
            return super().form_invalid(form)


class AdicionarPetServico(LoginRequiredMixin, CreateView):
    template_name = 'adicionarservico.html'
    model = Grade
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servico = self.kwargs['pk']

        pets = Pet.objects.all()
        pets_cadastrados = Grade.objects.filter(
            servico__pk=servico).values('pet')
        pets_nao_vinculados = pets.exclude(pk__in=pets_cadastrados)

        context['pets_nao_vinculados'] = pets_nao_vinculados
        context['servico'] = servico
        return context

    def form_valid(self, form):
        grade = form.save(commit=False)
        pet_id = self.request.POST.get('pet_id')
        servico = self.kwargs['pk']

        if Grade.objects.filter(servico=servico, pet=pet_id).exists():
            messages.error(
                self.request, 'Já existe uma associação para este pet e serviço.')
            return self.form_invalid(form)

        grade.servico = Servico.objects.get(pk=servico)
        grade.pet = Pet.objects.get(pk=pet_id)
        grade.save()

        success_url = reverse('servicos:verservicos',
                              kwargs={'pk': servico}) + '?mensagem=Pet adicionado ao serviço com sucesso!'
        return redirect(success_url)


class DeletarPetServico(LoginRequiredMixin, DeleteView):
    template_name = 'deletarpetservico.html'
    model = Grade

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servico = self.kwargs['servico_pk']
        context['servico'] = servico
        return context

    def get_success_url(self):
        grade = Grade.objects.get(pk=self.kwargs['pk'])
        cliente = grade.pet.tutor
        pagamento = Pagamento.objects.filter(
            cliente=cliente).order_by('-dia_vencimento').first()
        hoje = datetime.now().date()
        if pagamento.dia_vencimento < hoje + timedelta(days=25) and pagamento.total_pagamento > 0:
            pagamento.total_pagamento -= grade.servico.valor
            pagamento.save()

        servico = self.kwargs['servico_pk']
        success_url = reverse('servicos:verservicos', kwargs={'pk': servico})
        return success_url
