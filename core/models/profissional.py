from django.db import models
from django.utils import timezone


class Profissional(models.Model):
    usuario = models.OneToOneField(
        'core.Usuario', on_delete=models.CASCADE, related_name='profissional'
    )
    especialidade = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    experiencia = models.PositiveIntegerField(default=0)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at')

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'

    def __str__(self):
        return f'{self.usuario.get_full_name()} — Profissional'
