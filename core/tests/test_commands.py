"""
Testes de integração — management commands.
"""
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from core.models.usuario import Usuario
from core.models.servico import Servico


class SeedServicoCommandTest(TestCase):

    def test_cria_5_servicos(self):
        call_command('seed_servicos', stdout=StringIO())
        self.assertEqual(Servico.objects.count(), 5)

    def test_nomes_dos_servicos(self):
        call_command('seed_servicos', stdout=StringIO())
        nomes = set(Servico.objects.values_list('nome', flat=True))
        esperados = {'Box Braids', 'Knotless Braids', 'Trança Nagô',
                     'Twist (Tranças de Dois Fios)', 'Tranças Fulani'}
        self.assertEqual(nomes, esperados)

    def test_idempotente_nao_duplica(self):
        call_command('seed_servicos', stdout=StringIO())
        call_command('seed_servicos', stdout=StringIO())
        self.assertEqual(Servico.objects.count(), 5)

    def test_servicos_criados_como_ativos(self):
        call_command('seed_servicos', stdout=StringIO())
        inativos = Servico.objects.filter(status=False).count()
        self.assertEqual(inativos, 0)

    def test_saida_lista_servicos_criados(self):
        out = StringIO()
        call_command('seed_servicos', stdout=out)
        saida = out.getvalue()
        self.assertIn('Box Braids', saida)


class SeedUsuarioCommandTest(TestCase):

    def test_cria_usuario_com_defaults(self):
        call_command('seed_usuario', stdout=StringIO())
        self.assertTrue(Usuario.objects.filter(email='admin@meyristudio.com').exists())

    def test_usuario_criado_e_profissional(self):
        call_command('seed_usuario', stdout=StringIO())
        u = Usuario.objects.get(email='admin@meyristudio.com')
        self.assertEqual(u.tipo, 'profissional')

    def test_usuario_criado_com_status_ativo(self):
        call_command('seed_usuario', stdout=StringIO())
        u = Usuario.objects.get(email='admin@meyristudio.com')
        self.assertTrue(u.status)

    def test_usuario_pode_autenticar(self):
        call_command('seed_usuario', stdout=StringIO())
        from django.contrib.auth import authenticate
        u = authenticate(username='admin@meyristudio.com', password='admin123')
        self.assertIsNotNone(u)

    def test_idempotente_nao_duplica(self):
        call_command('seed_usuario', stdout=StringIO())
        call_command('seed_usuario', stdout=StringIO())
        self.assertEqual(Usuario.objects.filter(email='admin@meyristudio.com').count(), 1)

    def test_email_personalizado(self):
        call_command('seed_usuario',
                     '--email', 'custom@test.com',
                     '--password', 'pass456',
                     stdout=StringIO())
        self.assertTrue(Usuario.objects.filter(email='custom@test.com').exists())
