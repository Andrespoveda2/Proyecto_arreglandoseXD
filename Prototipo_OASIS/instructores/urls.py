# instructores/urls.py

from django.urls import path
from . import views

app_name = 'instructores'

urlpatterns = [
    # Vistas de Instructor
    path('dashboard/', views.dashboard_instructor, name='dashboard_instructor'),
    path('asignaciones/', views.proyectos_asignados, name='proyectos_asignados'),
    path('avance/<int:pk>/', views.seguimiento_avance, name='seguimiento_avance'),
]
