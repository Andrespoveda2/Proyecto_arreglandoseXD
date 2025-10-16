# instructores/urls.py

from django.urls import path
from . import views

app_name = 'instructores'

urlpatterns = [
    # Vistas de Instructor
    path('dashboard/', views.dashboard_instructor, name='dashboard_instructor'),
    path('perfil/', views.perfil_instructor, name='mi_perfil_instructor'),
    path('editar_perfil/', views.editar_perfil_instructor, name='editar_perfil_instructor'),
    path('perfil/<int:perfil_id>/', views.perfil_instructor, name='perfil_instructor'),
    path('asignaciones/', views.proyectos_asignados, name='proyectos_asignados'),
    path('avance/<int:pk>/', views.seguimiento_avance, name='seguimiento_avance'),
    
    path('proyectos_disponibles/', views.listar_proyectos, name='proyectos_disponibles'),
    path('proyecto/<int:pk>/', views.detalle_proyecto_instructor, name='detalle_proyecto_instructor'),
    path('proyecto/<int:pk>/postular/', views.postular_proyecto_instructor, name='postular_proyecto_instructor'),
]