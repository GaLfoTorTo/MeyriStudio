from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'w-full'})
    )
    password = forms.CharField(
        label='Senha de acesso',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••••', 'class': 'w-full'})
    )
