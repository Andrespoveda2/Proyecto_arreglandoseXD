from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('programas/', views.gestion_programas, name='gestion_programas'),
    path('reportes/', views.reportes, name='reportes'),

]

