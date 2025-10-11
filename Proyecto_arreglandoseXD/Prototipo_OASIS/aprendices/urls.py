from django.urls import path
from . import views

app_name = 'aprendices'  # para nombres de espacio en URLs

urlpatterns = [
    path('dashboard/', views.dashboard_aprendiz, name='dashboard_aprendiz'),
    path('proyectos/', views.ver_proyectos, name='ver_proyectos'),
    path('perfil/', views.perfil_aprendiz, name='perfil_aprendiz'),
    path('detalle_proyecto/<int:pk>/', views.detalle_proyecto, name='detalle_proyecto'),

    # ✅ Nueva ruta para registrar aprendizajes
    #path('registrar_aprendizaje/', views.registrar_aprendizaje, name='registrar_aprendizaje'),
]
