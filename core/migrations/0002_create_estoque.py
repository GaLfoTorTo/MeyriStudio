import django.utils.timezone
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
                ('preco', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('unidade', models.CharField(
                    choices=[('unidade', 'Unidade'), ('pacote', 'Pacote'), ('metro', 'Metro'), ('grama', 'Grama')],
                    default='unidade',
                    max_length=20,
                )),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'Estoque',
                'verbose_name_plural': 'Estoques',
            },
        ),
    ]
