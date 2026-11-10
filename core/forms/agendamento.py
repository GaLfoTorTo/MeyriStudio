from django import forms
from core.models.agendamento import Agendamento


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = [
            'cliente', 'profissional', 'servico',
            'data_hora_inicio', 'data_hora_fim',
            'valor_total', 'sinal_pago', 'material', 'observacoes',
        ]
        widgets = {
            'data_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
