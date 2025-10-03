from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('programas/', views.gestion_programas, name='gestion_programas'),
    path('reportes/', views.reportes, name='reportes'),
    
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]

