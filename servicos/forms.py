from django import forms

from servicos.models import Pet


class DateInput(forms.DateInput):
    input_type = 'date'

class EditarPetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['imagem', 'nome', 'data_nascimento', 'genero',
                  'raca', 'descricao_medica', 'castrado', 'turma']
        widgets = {
            'data_nascimento': DateInput(),
        }