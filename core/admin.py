from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models.usuario import Usuario
from core.models.profissional import Profissional
from core.models.cliente import Cliente
from core.models.servico import Servico
from core.models.agendamento import Agendamento
from core.models.estoque import Estoque


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo', 'telefone', 'is_active']
    list_filter = ['tipo', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('MeyriStudio', {'fields': ('tipo', 'telefone', 'foto')}),
    )


admin.site.register(Profissional)
admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Estoque)
