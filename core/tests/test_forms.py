"""
Testes unitários — forms validados sem banco de dados.
"""
import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from core.forms.auth import LoginForm
from core.forms.agendamento import AgendamentoForm
from core.models.usuario import Usuario
from core.models.servico import Servico
from core.models.cliente import Cliente
from core.models.profissional import Profissional


class LoginFormTest(TestCase):

    def test_campos_presentes(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)

    def test_campo_username_e_email_field(self):
        from django import forms as dj_forms
        form = LoginForm()
        self.assertIsInstance(form.fields['username'], dj_forms.EmailField)

    def test_form_vazio_e_invalido(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_sem_senha_e_invalido(self):
        form = LoginForm(data={'username': 'a@b.com', 'password': ''})
        self.assertFalse(form.is_valid())


class AgendamentoFormTest(TestCase):

    def setUp(self):
        u_prof = Usuario.objects.create_user(
            email='p@t.com', username='p', password='123', tipo='profissional'
        )
        u_cli = Usuario.objects.create_user(
            email='c@t.com', username='c', password='123', tipo='cliente'
        )
        self.profissional = Profissional.objects.create(usuario=u_prof)
        self.cliente = Cliente.objects.create(usuario=u_cli)
        self.servico = Servico.objects.create(
            nome='Box Braids', duracao=Decimal('6.00'), preco=Decimal('280.00')
        )

    def _dados_validos(self):
        inicio = timezone.now() + datetime.timedelta(hours=1)
        return {
            'cliente': self.cliente.pk,
            'profissional': self.profissional.pk,
            'servico': self.servico.pk,
            'inicio': inicio.strftime('%Y-%m-%dT%H:%M'),
            'fim': (inicio + datetime.timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M'),
            'valor': '280.00',
            'material': 'cliente_traz',
            'observacoes': '',
        }

    def test_dados_validos(self):
        form = AgendamentoForm(data=self._dados_validos())
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_sem_cliente_invalido(self):
        dados = self._dados_validos()
        dados.pop('cliente')
        form = AgendamentoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('cliente', form.errors)

    def test_sem_valor_invalido(self):
        dados = self._dados_validos()
        dados['valor'] = ''
        form = AgendamentoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)

    def test_campos_do_form(self):
        form = AgendamentoForm()
        for campo in ('cliente', 'profissional', 'servico', 'inicio', 'fim', 'valor'):
            self.assertIn(campo, form.fields)
