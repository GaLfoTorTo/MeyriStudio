from django import forms
from core.models.agendamento import Agendamento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'cliente', 'profissional', 'servico',
            'inicio', 'fim',
            'valor', 'material', 'observacoes',
        ]
        widgets = {
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
