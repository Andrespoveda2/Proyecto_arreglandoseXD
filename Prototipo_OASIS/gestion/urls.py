from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('dashboard/', views.dashboard_gestion, name='dashboard_gestion'),
    path('usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('proyectos_asignados/', views.proyectos_asignados, name='proyectos_asignados'),
    path('seguimiento/<int:pk>/', views.seguimiento_avance, name='seguimiento_avance'),
]

