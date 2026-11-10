from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Agendamento


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='E-mail profissional',
        widget=forms.TextInput(attrs={'placeholder': 'seu@email.com', 'class': 'w-full'})
    )
    password = forms.CharField(
        label='Senha de acesso',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••••', 'class': 'w-full'})
    )


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'profissional', 'servico', 'data_hora_inicio', 'data_hora_fim',
                  'valor_total', 'sinal_pago', 'material', 'observacoes']
        widgets = {
            'data_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_hora_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
