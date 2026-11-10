import django.db.models.deletion
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
                ('data_hora_inicio', models.DateTimeField()),
                ('data_hora_fim', models.DateTimeField()),
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
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sinal_pago', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('material', models.CharField(
                    choices=[('cliente_traz', 'Cliente Traz'), ('salao_fornece', 'Salão Fornece')],
                    default='cliente_traz',
                    max_length=20,
                )),
                ('observacoes', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
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
            ],
            options={
                'verbose_name': 'Agendamento',
                'verbose_name_plural': 'Agendamentos',
                'ordering': ['data_hora_inicio'],
            },
        ),
    ]
