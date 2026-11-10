from .auth import login_view, logout_view
from .home import home_view
from .agenda import agenda_view, agendamentos_json, criar_agendamento

__all__ = [
    'login_view', 'logout_view',
    'home_view',
    'agenda_view', 'agendamentos_json', 'criar_agendamento',
]
