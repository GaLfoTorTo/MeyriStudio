from django.urls import path

from core.views.auth import login_view, logout_view
from core.views.home import home_view
from core.views.agenda import agenda_view, agendamentos_json, criar_agendamento

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('agenda/', agenda_view, name='agenda'),
    path('api/agendamentos/', agendamentos_json, name='agendamentos_json'),
    path('api/agendamentos/criar/', criar_agendamento, name='criar_agendamento'),
]
