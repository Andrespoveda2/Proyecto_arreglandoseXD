from django.urls import path
from . import views

urlpatterns = [
    # Página para elegir tipo de registro
    path('elegir/', views.elegir_registro, name='elegir_registro'),

    # Formularios separados por rol
    path('registro/aprendiz/', views.registro_aprendiz, name='registro_aprendiz'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro/instructor/', views.registro_instructor, name='registro_instructor'),

    # Login único
    path('login/', views.login_view, name='login'),
]
