import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from core.models.agendamento import Agendamento
from core.models.cliente import Cliente
from core.models.profissional import Profissional


def _semana_do_dia(data):
    inicio = data - datetime.timedelta(days=data.weekday())
    return [(inicio + datetime.timedelta(days=i)).day for i in range(7)]


@login_required
def home_view(request):
    hoje = timezone.localdate()
    inicio_dia = timezone.make_aware(datetime.datetime.combine(hoje, datetime.time.min))
    fim_dia = timezone.make_aware(datetime.datetime.combine(hoje, datetime.time.max))
    agendamentos_hoje = Agendamento.objects.filter(
        inicio__range=(inicio_dia, fim_dia)
    ).select_related('cliente__usuario', 'profissional__usuario', 'servico')

    if request.user.is_profissional():
        try:
            profissional = request.user.profissional
            agendamentos_hoje = agendamentos_hoje.filter(profissional=profissional)
        except Profissional.DoesNotExist:
            agendamentos_hoje = Agendamento.objects.none()

    proximo = agendamentos_hoje.filter(
        status__in=['confirmado', 'pendente'],
        inicio__gte=timezone.now()
    ).order_by('inicio').first()

    total_clientes = Cliente.objects.count()
    faturamento_hoje = agendamentos_hoje.filter(
        status='concluido'
    ).aggregate(total=Sum('valor'))['total'] or 0

    concluidos = agendamentos_hoje.filter(status='concluido').count()
    agendados = agendamentos_hoje.filter(status__in=['confirmado', 'pendente']).count()

    return render(request, 'core/home.html', {
        'agendamentos_hoje': agendamentos_hoje.order_by('inicio'),
        'hoje_semana': _semana_do_dia(hoje),
        'proximo': proximo,
        'total_clientes': total_clientes,
        'faturamento_hoje': faturamento_hoje,
        'concluidos': concluidos,
        'agendados': agendados,
        'hoje': hoje,
    })
