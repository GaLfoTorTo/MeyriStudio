"""
Testes de integração — views com banco de dados real (test DB).
Valida fluxo HTTP completo: request → view → template → response.
"""
import datetime
import json
from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from core.models.usuario import Usuario
from core.models.servico import Servico
from core.models.cliente import Cliente
from core.models.profissional import Profissional
from core.models.agendamento import Agendamento


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class BaseViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Profissional
        self.u_prof = Usuario.objects.create_user(
            email='prof@test.com',
            username='prof',
            password='senha123',
            tipo='profissional',
            first_name='Ana',
            status=True,
        )
        self.profissional = Profissional.objects.create(usuario=self.u_prof)

        # Cliente
        self.u_cli = Usuario.objects.create_user(
            email='cli@test.com',
            username='cli',
            password='senha123',
            tipo='cliente',
            first_name='Maria',
            status=True,
        )
        self.cliente = Cliente.objects.create(usuario=self.u_cli)

        # Serviço
        self.servico = Servico.objects.create(
            nome='Box Braids',
            duracao=Decimal('6.00'),
            preco=Decimal('280.00'),
            status=True,
        )

    def _login_prof(self):
        self.client.force_login(self.u_prof)

    def _login_cli(self):
        self.client.force_login(self.u_cli)

    def _make_agendamento(self):
        hoje = timezone.localdate()
        inicio = timezone.make_aware(
            datetime.datetime.combine(hoje, datetime.time(10, 0))
        )
        return Agendamento.objects.create(
            cliente=self.cliente,
            profissional=self.profissional,
            servico=self.servico,
            inicio=inicio,
            fim=inicio + datetime.timedelta(hours=6),
            valor=Decimal('280.00'),
        )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginViewTest(BaseViewTest):

    def test_get_retorna_200(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/login.html')

    def test_post_credenciais_validas_redireciona_home(self):
        resp = self.client.post(reverse('login'), {
            'username': 'prof@test.com',
            'password': 'senha123',
        })
        self.assertRedirects(resp, reverse('home'))

    def test_post_senha_errada_permanece_no_login(self):
        resp = self.client.post(reverse('login'), {
            'username': 'prof@test.com',
            'password': 'errada',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/login.html')

    def test_post_email_inexistente_permanece_no_login(self):
        resp = self.client.post(reverse('login'), {
            'username': 'naoexiste@test.com',
            'password': 'senha123',
        })
        self.assertEqual(resp.status_code, 200)

    def test_usuario_ja_autenticado_redireciona_home(self):
        self._login_prof()
        resp = self.client.get(reverse('login'))
        self.assertRedirects(resp, reverse('home'))

    def test_logout_redireciona_login(self):
        self._login_prof()
        resp = self.client.get(reverse('logout'))
        self.assertRedirects(resp, reverse('login'))


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

class HomeViewTest(BaseViewTest):

    def test_sem_autenticacao_redireciona_login(self):
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, f"{reverse('login')}?next={reverse('home')}")

    def test_autenticado_retorna_200(self):
        self._login_prof()
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/home.html')

    def test_contexto_contem_kpis(self):
        self._login_prof()
        resp = self.client.get(reverse('home'))
        for chave in ('agendamentos_hoje', 'total_clientes', 'faturamento_hoje',
                      'concluidos', 'agendados', 'hoje', 'hoje_semana'):
            self.assertIn(chave, resp.context, msg=f'Chave ausente no contexto: {chave}')

    def test_hoje_semana_tem_7_dias(self):
        self._login_prof()
        resp = self.client.get(reverse('home'))
        self.assertEqual(len(resp.context['hoje_semana']), 7)

    def test_faturamento_soma_apenas_concluidos(self):
        self._login_prof()
        ag = self._make_agendamento()
        ag.status = 'concluido'
        ag.save()
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.context['faturamento_hoje'], Decimal('280.00'))

    def test_profissional_ve_apenas_seus_agendamentos(self):
        self._login_prof()
        self._make_agendamento()
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.context['agendamentos_hoje'].count(), 1)


# ---------------------------------------------------------------------------
# Agenda
# ---------------------------------------------------------------------------

class AgendaViewTest(BaseViewTest):

    def test_sem_autenticacao_redireciona(self):
        resp = self.client.get(reverse('agenda'))
        self.assertEqual(resp.status_code, 302)

    def test_autenticado_retorna_200(self):
        self._login_prof()
        resp = self.client.get(reverse('agenda'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/agenda.html')

    def test_contexto_contem_servicos_profissionais_clientes(self):
        self._login_prof()
        resp = self.client.get(reverse('agenda'))
        for chave in ('servicos', 'profissionais', 'clientes', 'form'):
            self.assertIn(chave, resp.context)

    def test_servicos_so_ativos(self):
        Servico.objects.create(nome='Inativo', duracao=1, preco=100, status=False)
        self._login_prof()
        resp = self.client.get(reverse('agenda'))
        nomes = [s.nome for s in resp.context['servicos']]
        self.assertNotIn('Inativo', nomes)


# ---------------------------------------------------------------------------
# API: agendamentos_json
# ---------------------------------------------------------------------------

class AgendamentosJsonTest(BaseViewTest):

    def test_sem_autenticacao_redireciona(self):
        resp = self.client.get(reverse('agendamentos_json'))
        self.assertEqual(resp.status_code, 302)

    def test_retorna_json_vazio_sem_agendamentos(self):
        self._login_prof()
        resp = self.client.get(reverse('agendamentos_json'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_retorna_eventos_com_campos_fullcalendar(self):
        self._login_prof()
        self._make_agendamento()
        resp = self.client.get(reverse('agendamentos_json'))
        dados = resp.json()
        self.assertEqual(len(dados), 1)
        evento = dados[0]
        for campo in ('id', 'title', 'start', 'end', 'color', 'extendedProps'):
            self.assertIn(campo, evento, msg=f'Campo ausente no evento: {campo}')

    def test_extended_props_contem_status_e_valor(self):
        self._login_prof()
        self._make_agendamento()
        resp = self.client.get(reverse('agendamentos_json'))
        props = resp.json()[0]['extendedProps']
        self.assertIn('status', props)
        self.assertIn('valor', props)

    def test_content_type_e_json(self):
        self._login_prof()
        resp = self.client.get(reverse('agendamentos_json'))
        self.assertIn('application/json', resp['Content-Type'])


# ---------------------------------------------------------------------------
# API: criar_agendamento
# ---------------------------------------------------------------------------

class CriarAgendamentoTest(BaseViewTest):

    def _payload(self):
        inicio = timezone.now() + datetime.timedelta(hours=2)
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

    def test_get_retorna_405(self):
        self._login_prof()
        resp = self.client.get(reverse('criar_agendamento'))
        self.assertEqual(resp.status_code, 405)

    def test_sem_autenticacao_redireciona(self):
        resp = self.client.post(reverse('criar_agendamento'), self._payload())
        self.assertEqual(resp.status_code, 302)

    def test_post_valido_cria_agendamento(self):
        self._login_prof()
        resp = self.client.post(reverse('criar_agendamento'), self._payload())
        self.assertEqual(resp.status_code, 200)
        dados = resp.json()
        self.assertTrue(dados['success'])
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_post_invalido_retorna_erros(self):
        self._login_prof()
        resp = self.client.post(reverse('criar_agendamento'), {})
        self.assertEqual(resp.status_code, 400)
        dados = resp.json()
        self.assertFalse(dados['success'])
        self.assertIn('errors', dados)
