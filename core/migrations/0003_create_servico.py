from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_estoque'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('duracao_horas', models.DecimalField(decimal_places=2, max_digits=4)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
            },
        ),
    ]
