from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_CHOICES = [('profissional', 'Profissional'), ('cliente', 'Cliente')]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente')
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)

    def is_profissional(self):
        return self.tipo == 'profissional'
