from django.db import models


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

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'

    def __str__(self):
        return f"{self.nome} — {self.quantidade} {self.unidade}"

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.quantidade_minima
