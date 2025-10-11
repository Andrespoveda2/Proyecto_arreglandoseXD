from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Vistas de Módulos Principales
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('programas/', views.gestion_programas, name='gestion_programas'),
    path('sectores/', views.gestion_sectores, name='gestion_sectores'),
    path('reportes/', views.reportes, name='reportes'),
    
    # Vistas de Proyectos
    path('proyectos/pendientes/', views.proyectos_pendientes, name='proyectos_pendientes'), # Nueva URL agregada
    
    # Vistas CRUD de Usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]
