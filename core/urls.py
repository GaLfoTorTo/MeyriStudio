from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('agenda/', views.agenda_view, name='agenda'),
    path('api/agendamentos/', views.agendamentos_json, name='agendamentos_json'),
    path('api/agendamentos/criar/', views.criar_agendamento, name='criar_agendamento'),
]
