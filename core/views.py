from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count
import json

from .forms import LoginForm, AgendamentoForm
from .models import Agendamento, Profissional, Cliente, Servico


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    hoje = timezone.localdate()
    agendamentos_hoje = Agendamento.objects.filter(
        data_hora_inicio__date=hoje
    ).select_related('cliente__usuario', 'profissional__usuario', 'servico')

    if request.user.is_profissional():
        try:
            profissional = request.user.profissional
            agendamentos_hoje = agendamentos_hoje.filter(profissional=profissional)
        except Profissional.DoesNotExist:
            agendamentos_hoje = Agendamento.objects.none()

    proximo = agendamentos_hoje.filter(
        status__in=['confirmado', 'pendente'],
        data_hora_inicio__gte=timezone.now()
    ).order_by('data_hora_inicio').first()

    total_clientes = Cliente.objects.count()
    faturamento_hoje = agendamentos_hoje.filter(
        status='concluido'
    ).aggregate(total=Sum('valor_total'))['total'] or 0

    concluidos = agendamentos_hoje.filter(status='concluido').count()
    agendados = agendamentos_hoje.filter(status__in=['confirmado', 'pendente']).count()

    context = {
        'agendamentos_hoje': agendamentos_hoje.order_by('data_hora_inicio'),
        'proximo': proximo,
        'total_clientes': total_clientes,
        'faturamento_hoje': faturamento_hoje,
        'concluidos': concluidos,
        'agendados': agendados,
        'hoje': hoje,
    }
    return render(request, 'core/home.html', context)


@login_required
def agenda_view(request):
    servicos = Servico.objects.filter(ativo=True)
    profissionais = Profissional.objects.select_related('usuario').all()
    clientes = Cliente.objects.select_related('usuario').all()
    form = AgendamentoForm()

    context = {
        'servicos': servicos,
        'profissionais': profissionais,
        'clientes': clientes,
        'form': form,
    }
    return render(request, 'core/agenda.html', context)


@login_required
def agendamentos_json(request):
    agendamentos = Agendamento.objects.select_related(
        'cliente__usuario', 'servico'
    ).all()
    eventos = []
    STATUS_COLORS = {
        'pendente': '#d97706',
        'confirmado': '#2563eb',
        'em_andamento': '#7c3aed',
        'concluido': '#16a34a',
        'cancelado': '#dc2626',
    }
    for ag in agendamentos:
        eventos.append({
            'id': ag.id,
            'title': f"{ag.cliente.usuario.get_full_name()} - {ag.servico.nome}",
            'start': ag.data_hora_inicio.isoformat(),
            'end': ag.data_hora_fim.isoformat(),
            'color': STATUS_COLORS.get(ag.status, '#6b7280'),
            'extendedProps': {
                'status': ag.status,
                'valor': str(ag.valor_total),
            }
        })
    return JsonResponse(eventos, safe=False)


@login_required
def criar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save()
            return JsonResponse({'success': True, 'id': agendamento.id})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)
