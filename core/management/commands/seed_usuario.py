from django.core.management.base import BaseCommand

from core.models.usuario import Usuario


class Command(BaseCommand):
    help = 'Cria o primeiro usuário profissional do sistema'

    def add_arguments(self, parser):
        parser.add_argument('--email', default='admin@meyristudio.com')
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin123')
        parser.add_argument('--nome', default='Administrador')

    def handle(self, *args, **options):
        email = options['email']

        if Usuario.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(
                f'Usuário com e-mail "{email}" já existe. Nenhuma alteração feita.'
            ))
            return

        partes = options['nome'].split(' ', 1)
        first_name = partes[0]
        last_name = partes[1] if len(partes) > 1 else ''

        usuario = Usuario.objects.create_user(
            email=email,
            username=options['username'],
            password=options['password'],
            first_name=first_name,
            last_name=last_name,
            tipo='profissional',
            status=True,
        )

        self.stdout.write(self.style.SUCCESS(
            f'Usuário criado com sucesso!\n'
            f'  e-mail   : {usuario.email}\n'
            f'  username : {usuario.username}\n'
            f'  senha    : {options["password"]}\n'
            f'  tipo     : {usuario.tipo}\n'
        ))
