from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Profissional, Cliente, Servico, Agendamento, Estoque


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo', 'telefone', 'is_active']
    list_filter = ['tipo', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('AfroCare', {'fields': ('tipo', 'telefone', 'foto')}),
    )


admin.site.register(Profissional)
admin.site.register(Cliente)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Estoque)
