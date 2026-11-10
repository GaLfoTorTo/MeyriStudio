from django.db import models


class Cliente(models.Model):
    usuario = models.OneToOneField(
        'core.Usuario', on_delete=models.CASCADE, related_name='cliente'
    )
    observacoes_cabelo = models.TextField(blank=True)
    alerta_sensibilidade = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.usuario.get_full_name()} — Cliente"
