from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models.usuario import Usuario
from core.models.profissional import Profissional
from core.models.cliente import Cliente
from core.models.servico import Servico
from core.models.agendamento import Agendamento
from core.models.estoque import Estoque


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'tipo', 'telefone', 'status']
    list_filter = ['tipo', 'status']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Dados pessoais', {'fields': ('first_name', 'last_name', 'email', 'telefone', 'foto')}),
        ('MeyriStudio', {'fields': ('tipo', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tipo'),
        }),
    )
    ordering = ['username']


admin.site.register(Profissional)
admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Estoque)
