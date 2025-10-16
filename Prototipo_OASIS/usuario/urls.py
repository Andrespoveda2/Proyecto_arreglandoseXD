from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
# Nota: auth_views ya no es estrictamente necesario si usas solo LogoutView y tus vistas personalizadas.

app_name = 'auth' # Este es el namespace que usas en LOGIN_URL

urlpatterns = [
    # 1. Rutas de Registro
    path('elegir/', views.elegir_registro, name='elegir_registro'),
    path('registro/aprendiz/', views.registro_aprendiz, name='registro_aprendiz'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro/instructor/', views.registro_instructor, name='registro_instructor'),

    # 2. Rutas de Autenticación (Login y Logout)
    
    # A. VISTA DE LOGIN PERSONALIZADA (Tu vista, no la de Django)
    path('login/', views.login_view, name='login'), 
    
    # B. VISTA DE LOGOUT DE DJANGO
    # Muestra el template 'logged_out.html' y luego redirige a la raíz ('/')
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
    
    # 3. Otras Vistas
    path('contacto/', views.contacto_view, name='contacto'),
    path('manual_usuario/', views.manual_usuario, name='manual_usuario'),

    # 4. Rutas de restablecimiento de contraseña (si las tienes aquí)
    # Si las rutas de restablecimiento están en un urls.py diferente, elimina este include:
    # path('', include('django.contrib.auth.urls')), 
]
# NOTA: Asegúrate de que no haya código o líneas en blanco con espacios después del corchete final (])