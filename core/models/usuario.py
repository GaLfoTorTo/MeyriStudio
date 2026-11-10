import django.contrib.auth.validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, **extra_fields)


class Usuario(AbstractBaseUser):
    TIPO_CHOICES = [('profissional', 'Profissional'), ('cliente', 'Cliente')]

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username',
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        error_messages={'unique': 'A user with that username already exists.'},
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='last name')
    email = models.EmailField(blank=True, verbose_name='email address')
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='created at')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='updated at')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username

    @property
    def is_active(self):
        return self.status

    @property
    def is_staff(self):
        return self.tipo == 'profissional'

    def is_profissional(self):
        return self.tipo == 'profissional'

    def __str__(self):
        return self.get_full_name()
