from django.db import models
from django.utils import timezone


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
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidade = models.CharField(max_length=20, choices=UNIDADE_CHOICES, default='unidade')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at')

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f'{self.nome} — {self.quantidade} {self.unidade}'
