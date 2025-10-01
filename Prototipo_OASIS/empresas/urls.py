from django.urls import path
from . import views

app_name = 'empresas'  # Para namespace

urlpatterns = [
    path('dashboard/', views.dashboard_empresa, name='dashboard_empresa'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar_proyecto/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('ver_solicitudes/', views.ver_solicitudes, name='ver_solicitudes'),
]
