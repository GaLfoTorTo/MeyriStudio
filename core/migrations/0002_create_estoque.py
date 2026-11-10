from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_create_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('quantidade', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('unidade', models.CharField(
                    choices=[('unidade', 'Unidade'), ('pacote', 'Pacote'), ('metro', 'Metro'), ('grama', 'Grama')],
                    default='unidade',
                    max_length=20,
                )),
                ('preco_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantidade_minima', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Estoque',
                'verbose_name_plural': 'Estoques',
            },
        ),
    ]
