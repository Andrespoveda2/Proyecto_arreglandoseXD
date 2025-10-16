from django.urls import path
from . import views
from .views import DetalleUsuarioView

app_name = 'gestion'

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),

    # Usuarios
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/', DetalleUsuarioView.as_view(), name='detalle_usuario'),

    # Programas
    path('programas/', views.gestion_programas, name='gestion_programas'),
    path('programas/editar/<int:pk>/', views.editar_programa, name='editar_programa'),
    path('programas/eliminar/<int:pk>/', views.eliminar_programa, name='eliminar_programa'),

    # Sectores
    path('sectores/', views.gestion_sectores, name='gestion_sectores'),
    path('sectores/editar/<int:pk>/', views.editar_sector, name='editar_sector'),
    path('sectores/eliminar/<int:pk>/', views.eliminar_sector, name='eliminar_sector'),

    # Proyectos
    path('proyectos/', views.revisar_solicitudes, name='revisar_solicitudes'),
    path('proyectos/aprobar/<int:pk>/', views.aprobar_proyecto, name='aprobar_proyecto'),
    path('proyectos/rechazar/<int:pk>/', views.rechazar_proyecto, name='rechazar_proyecto'),

    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]