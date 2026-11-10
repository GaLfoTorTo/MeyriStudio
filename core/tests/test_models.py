"""
Testes unitários — models isolados, sem dependência de views ou URLs.
"""
import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from core.models.usuario import Usuario
from core.models.estoque import Estoque
from core.models.servico import Servico
from core.models.cliente import Cliente
from core.models.profissional import Profissional
from core.models.agendamento import Agendamento


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_usuario(email='user@test.com', tipo='cliente', **kwargs):
    return Usuario.objects.create_user(
        email=email,
        username=kwargs.pop('username', email.split('@')[0]),
        password='senha123',
        tipo=tipo,
        status=True,
        **kwargs,
    )


def make_servico():
    return Servico.objects.create(
        nome='Box Braids',
        duracao=Decimal('6.00'),
        preco=Decimal('280.00'),
        status=True,
    )


def make_cliente(usuario=None):
    if usuario is None:
        usuario = make_usuario(email='cliente@test.com', tipo='cliente')
    return Cliente.objects.create(usuario=usuario)


def make_profissional(usuario=None):
    if usuario is None:
        usuario = make_usuario(email='prof@test.com', tipo='profissional')
    return Profissional.objects.create(usuario=usuario)


def make_agendamento(cliente=None, profissional=None, servico=None):
    if cliente is None:
        cliente = make_cliente()
    if profissional is None:
        profissional = make_profissional()
    if servico is None:
        servico = make_servico()
    inicio = timezone.now() + datetime.timedelta(hours=1)
    return Agendamento.objects.create(
        cliente=cliente,
        profissional=profissional,
        servico=servico,
        inicio=inicio,
        fim=inicio + datetime.timedelta(hours=6),
        valor=Decimal('280.00'),
    )


# ---------------------------------------------------------------------------
# Usuario
# ---------------------------------------------------------------------------

class UsuarioManagerTest(TestCase):

    def test_create_user_sem_email_levanta_erro(self):
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(email='', username='x', password='123')

    def test_create_user_normaliza_email(self):
        u = make_usuario(email='UPPER@TEST.COM')
        self.assertEqual(u.email, 'UPPER@test.com')

    def test_create_superuser(self):
        u = Usuario.objects.create_superuser(
            email='super@test.com', username='super', password='123'
        )
        self.assertIsNotNone(u.pk)


class UsuarioModelTest(TestCase):

    def setUp(self):
        self.profissional = make_usuario(
            email='prof@test.com',
            username='prof',
            tipo='profissional',
            first_name='Ana',
            last_name='Souza',
        )
        self.cliente = make_usuario(
            email='cli@test.com',
            username='cli',
            tipo='cliente',
        )

    def test_is_profissional_retorna_true(self):
        self.assertTrue(self.profissional.is_profissional())

    def test_is_profissional_retorna_false_para_cliente(self):
        self.assertFalse(self.cliente.is_profissional())

    def test_is_active_reflete_status(self):
        self.assertTrue(self.profissional.is_active)
        self.profissional.status = False
        self.assertFalse(self.profissional.is_active)

    def test_is_staff_para_profissional(self):
        self.assertTrue(self.profissional.is_staff)
        self.assertFalse(self.cliente.is_staff)

    def test_get_full_name_com_nome(self):
        self.assertEqual(self.profissional.get_full_name(), 'Ana Souza')

    def test_get_full_name_sem_nome_retorna_username(self):
        u = make_usuario(email='noname@test.com', username='noname')
        self.assertEqual(u.get_full_name(), 'noname')

    def test_get_short_name(self):
        self.assertEqual(self.profissional.get_short_name(), 'Ana')

    def test_str(self):
        self.assertEqual(str(self.profissional), 'Ana Souza')

    def test_username_field_e_email(self):
        self.assertEqual(Usuario.USERNAME_FIELD, 'email')

    def test_email_e_unico(self):
        field = Usuario._meta.get_field('email')
        self.assertTrue(field.unique)


# ---------------------------------------------------------------------------
# Estoque
# ---------------------------------------------------------------------------

class EstoqueModelTest(TestCase):

    def test_str(self):
        e = Estoque.objects.create(
            nome='Cabelo Sintético',
            quantidade=Decimal('10.00'),
            unidade='pacote',
        )
        self.assertIn('Cabelo Sintético', str(e))
        self.assertIn('pacote', str(e))

    def test_valores_padrao(self):
        e = Estoque.objects.create(nome='Item')
        self.assertEqual(e.quantidade, Decimal('0'))
        self.assertEqual(e.unidade, 'unidade')

    def test_created_at_preenchido_automaticamente(self):
        e = Estoque.objects.create(nome='Item')
        self.assertIsNotNone(e.created_at)


# ---------------------------------------------------------------------------
# Servico
# ---------------------------------------------------------------------------

class ServicoModelTest(TestCase):

    def test_str(self):
        s = make_servico()
        self.assertIn('Box Braids', str(s))
        self.assertIn('280', str(s))

    def test_status_padrao_ativo(self):
        s = Servico.objects.create(nome='Teste', duracao=1, preco=100)
        self.assertTrue(s.status)


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------

class ClienteModelTest(TestCase):

    def test_str_contem_nome_e_cliente(self):
        u = make_usuario(
            email='c@test.com', username='c',
            first_name='Maria', last_name='Lima', tipo='cliente',
        )
        c = Cliente.objects.create(usuario=u)
        self.assertIn('Maria Lima', str(c))
        self.assertIn('Cliente', str(c))

    def test_campos_opcionais_em_branco(self):
        c = make_cliente()
        self.assertEqual(c.tipo_cabelo, '')
        self.assertEqual(c.sensibilidade, '')

    def test_relacionamento_one_to_one(self):
        c = make_cliente()
        self.assertEqual(c.usuario.cliente, c)


# ---------------------------------------------------------------------------
# Profissional
# ---------------------------------------------------------------------------

class ProfissionalModelTest(TestCase):

    def test_str(self):
        u = make_usuario(
            email='p@test.com', username='p',
            first_name='João', last_name='Silva', tipo='profissional',
        )
        p = Profissional.objects.create(usuario=u)
        self.assertIn('João Silva', str(p))
        self.assertIn('Profissional', str(p))

    def test_avaliacao_padrao(self):
        p = make_profissional()
        self.assertEqual(p.avaliacao, Decimal('5.00'))

    def test_experiencia_padrao_zero(self):
        p = make_profissional()
        self.assertEqual(p.experiencia, 0)


# ---------------------------------------------------------------------------
# Agendamento
# ---------------------------------------------------------------------------

class AgendamentoModelTest(TestCase):

    def setUp(self):
        self.ag = make_agendamento()

    def test_str_contem_servico_e_data(self):
        s = str(self.ag)
        self.assertIn('Box Braids', s)

    def test_status_padrao_pendente(self):
        self.assertEqual(self.ag.status, 'pendente')

    def test_material_padrao(self):
        self.assertEqual(self.ag.material, 'cliente_traz')

    def test_ordering_por_inicio(self):
        meta_ordering = Agendamento._meta.ordering
        self.assertIn('inicio', meta_ordering)

    def test_created_at_preenchido(self):
        self.assertIsNotNone(self.ag.created_at)
