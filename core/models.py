from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_CHOICES = [('profissional', 'Profissional'), ('cliente', 'Cliente')]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente')
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)

    def is_profissional(self):
        return self.tipo == 'profissional'


class Profissional(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='profissional')
    especialidade = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    anos_experiencia = models.PositiveIntegerField(default=0)
    avaliacao_media = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    cadeira_ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - Profissional"


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente')
    observacoes_cabelo = models.TextField(blank=True)
    alerta_sensibilidade = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - Cliente"


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    duracao_horas = models.DecimalField(max_digits=4, decimal_places=2)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    MATERIAL_CHOICES = [
        ('cliente_traz', 'Cliente Traz'),
        ('salao_fornece', 'Salão Fornece'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    sinal_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='cliente_traz')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.servico} em {self.data_hora_inicio:%d/%m/%Y %H:%M}"

    @property
    def saldo_restante(self):
        return self.valor_total - self.sinal_pago


class Estoque(models.Model):
    UNIDADE_CHOICES = [
        ('unidade', 'Unidade'),
        ('pacote', 'Pacote'),
        ('metro', 'Metro'),
        ('grama', 'Grama'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidade = models.CharField(max_length=20, choices=UNIDADE_CHOICES, default='unidade')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_minima = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - {self.quantidade} {self.unidade}"

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.quantidade_minima
