from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='E-mail profissional',
        widget=forms.TextInput(attrs={'placeholder': 'seu@email.com', 'class': 'w-full'})
    )
    password = forms.CharField(
        label='Senha de acesso',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••••', 'class': 'w-full'})
    )
