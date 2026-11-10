import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_create_profissional'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField()),
                ('fim', models.DateTimeField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observacoes', models.TextField(blank=True)),
                ('material', models.CharField(
                    choices=[('cliente_traz', 'Cliente Traz'), ('salao_fornece', 'Salão Fornece')],
                    default='cliente_traz',
                    max_length=20,
                )),
                ('status', models.CharField(
                    choices=[
                        ('pendente', 'Pendente'),
                        ('confirmado', 'Confirmado'),
                        ('em_andamento', 'Em Andamento'),
                        ('concluido', 'Concluído'),
                        ('cancelado', 'Cancelado'),
                    ],
                    default='pendente',
                    max_length=20,
                )),
                ('cliente', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='agendamentos',
                    to='core.cliente',
                )),
                ('profissional', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='agendamentos',
                    to='core.profissional',
                )),
                ('servico', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.servico',
                )),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'ordering': ['data_hora_inicio'],
            },
        ),
    ]
