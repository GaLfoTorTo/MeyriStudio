from django.core.management.base import BaseCommand

from core.models.servico import Servico

SERVICOS = [
    {
        'nome': 'Box Braids',
        'descricao': (
            'Tranças soltas individuais com extensão sintética, médias ou compridas. '
            'Uma das técnicas mais populares, versátil para qualquer ocasião.'
        ),
        'duracao': 6.00,
        'preco': 280.00,
    },
    {
        'nome': 'Knotless Braids',
        'descricao': (
            'Variação das box braids sem nó na raiz, resultando em tranças mais leves, '
            'confortáveis e com acabamento mais natural. Menor tensão no couro cabeludo.'
        ),
        'duracao': 7.00,
        'preco': 350.00,
    },
    {
        'nome': 'Trança Nagô',
        'descricao': (
            'Tranças finas feitas na própria raiz do cabelo, em fileiras paralelas. '
            'Técnica tradicional africana, discreta e de longa duração.'
        ),
        'duracao': 3.00,
        'preco': 150.00,
    },
    {
        'nome': 'Twist (Tranças de Dois Fios)',
        'descricao': (
            'Técnica de torção com dois fios que cria um visual moderno e volumoso. '
            'Pode ser feita com cabelo natural ou com extensão.'
        ),
        'duracao': 4.00,
        'preco': 220.00,
    },
    {
        'nome': 'Tranças Fulani',
        'descricao': (
            'Penteado de origem africana com tranças finas no centro da cabeça e '
            'detalhes laterais, frequentemente adornado com miçangas e fios coloridos.'
        ),
        'duracao': 5.00,
        'preco': 300.00,
    },
]


class Command(BaseCommand):
    help = 'Cria os 5 serviços padrão de tranças no sistema'

    def handle(self, *args, **options):
        criados = 0
        existentes = 0

        for dados in SERVICOS:
            obj, created = Servico.objects.get_or_create(
                nome=dados['nome'],
                defaults={
                    'descricao': dados['descricao'],
                    'duracao': dados['duracao'],
                    'preco': dados['preco'],
                    'status': True,
                },
            )
            if created:
                criados += 1
                self.stdout.write(f"  ✓ {obj.nome} — R$ {obj.preco:.2f} ({obj.duracao}h)")
            else:
                existentes += 1
                self.stdout.write(self.style.WARNING(f"  ~ {obj.nome} já existe, pulando."))

        self.stdout.write('')
        if criados:
            self.stdout.write(self.style.SUCCESS(f'{criados} serviço(s) criado(s).'))
        if existentes:
            self.stdout.write(f'{existentes} serviço(s) já existiam.')
