from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'auth' # Este es el namespace que usamos en LOGIN_URL


urlpatterns = [
    # Página para elegir tipo de registro
    path('elegir/', views.elegir_registro, name='elegir_registro'),

    # Formularios separados por rol
    path('registro/aprendiz/', views.registro_aprendiz, name='registro_aprendiz'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro/instructor/', views.registro_instructor, name='registro_instructor'),

    # Login único
    path('login/', views.login_view, name='login'), # TU VISTA PERSONALIZADA

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
]
