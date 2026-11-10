from django.db import models


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
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    sinal_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='cliente_traz')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_hora_inicio']

    def __str__(self):
        return f"{self.cliente} — {self.servico} em {self.data_hora_inicio:%d/%m/%Y %H:%M}"

    @property
    def saldo_restante(self):
        return self.valor_total - self.sinal_pago
