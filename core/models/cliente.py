from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    usuario = models.OneToOneField(
        'core.Usuario', on_delete=models.CASCADE, related_name='cliente'
    )
    tipo_cabelo = models.TextField(blank=True)
    sensibilidade = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'{self.usuario.get_full_name()} — Cliente'
