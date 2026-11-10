from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from core.forms.agendamento import AgendamentoForm
from core.models.agendamento import Agendamento
from core.models.cliente import Cliente
from core.models.profissional import Profissional
from core.models.servico import Servico

STATUS_COLORS = {
    'pendente': '#d97706',
    'confirmado': '#2563eb',
    'em_andamento': '#7c3aed',
    'concluido': '#16a34a',
    'cancelado': '#dc2626',
}


@login_required
def agenda_view(request):
    return render(request, 'core/agenda.html', {
        'servicos': Servico.objects.filter(ativo=True),
        'profissionais': Profissional.objects.select_related('usuario').all(),
        'clientes': Cliente.objects.select_related('usuario').all(),
        'form': AgendamentoForm(),
    })


@login_required
def agendamentos_json(request):
    agendamentos = Agendamento.objects.select_related('cliente__usuario', 'servico').all()
    eventos = [
        {
            'id': ag.id,
            'title': f"{ag.cliente.usuario.get_full_name()} — {ag.servico.nome}",
            'start': ag.data_hora_inicio.isoformat(),
            'end': ag.data_hora_fim.isoformat(),
            'color': STATUS_COLORS.get(ag.status, '#6b7280'),
            'extendedProps': {'status': ag.status, 'valor': str(ag.valor_total)},
        }
        for ag in agendamentos
    ]
    return JsonResponse(eventos, safe=False)


@login_required
def criar_agendamento(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    form = AgendamentoForm(request.POST)
    if form.is_valid():
        agendamento = form.save()
        return JsonResponse({'success': True, 'id': agendamento.id})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
