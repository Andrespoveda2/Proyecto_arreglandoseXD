# instructores/urls.py

from django.urls import path
from . import views

app_name = 'instructores'

urlpatterns = [
    # Vistas de Admin
    path('admin/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('admin/usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('admin/programas/', views.gestion_programas, name='gestion_programas'),
    path('admin/reportes/', views.reportes, name='reportes'),

    # Vistas de Instructor
    path('dashboard/', views.dashboard_instructor, name='dashboard_instructor'),
    path('solicitudes/', views.gestionar_solicitudes, name='gestionar_solicitudes'),
    path('asignar/', views.asignar_proyectos, name='asignar_proyectos'),
]
