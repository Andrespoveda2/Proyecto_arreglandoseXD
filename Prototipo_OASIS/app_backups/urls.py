from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_backups, name='lista_backups'),
    path('crear/', views.crear_backup_view, name='crear_backup'),
    path('eliminar/<int:backup_id>/', views.eliminar_backup_view, name='eliminar_backup'),
    path('restaurar/<int:backup_id>/', views.restaurar_backup_view, name='restaurar_backup'),
]
