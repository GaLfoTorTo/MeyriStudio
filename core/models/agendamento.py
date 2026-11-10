from django.db import models
from django.utils import timezone


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

    cliente = models.ForeignKey(
        'core.Cliente', on_delete=models.CASCADE, related_name='agendamentos'
    )
    profissional = models.ForeignKey(
        'core.Profissional', on_delete=models.CASCADE, related_name='agendamentos'
    )
    servico = models.ForeignKey('core.Servico', on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='cliente_traz')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['inicio']

    def __str__(self):
        return f'{self.cliente} — {self.servico} em {self.inicio:%d/%m/%Y %H:%M}'
