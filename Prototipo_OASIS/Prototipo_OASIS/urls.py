"""
URL configuration for Prototipo_OASIS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Configuración del URL Resolver principal
urlpatterns = [
    # Admin nativo de Django
    path('superadmin/', admin.site.urls), 
    
    # 1. Rutas Públicas (App home)
    path('', include(('home.urls', 'home'), namespace='home')),

    # 2. Rutas de Autenticación Personalizadas (App usuario) - Login, Registro, etc.
    path('auth/', include(('usuario.urls', 'auth'), namespace='auth')),

    # 3. Rutas de autenticación integradas de Django (para "Olvidé mi contraseña")
    # Se montan en 'accounts/' para no interferir con nuestras rutas 'auth/'.
    # Restablecer Contraseña (Paso 1: Solicitar Correo)
    path('accounts/password_reset/', 
          auth_views.PasswordResetView.as_view(
              template_name='password_reset.html',
              email_template_name='password_reset_email.html',
              # Usamos reverse_lazy para evitar importaciones circulares
              success_url='/accounts/password_reset/done/' 
          ), name='password_reset'),
          
    # Notificación de Correo Enviado (Paso 2: Confirmación)
    path('accounts/password_reset/done/', 
          auth_views.PasswordResetDoneView.as_view(
              template_name='password_reset_done.html'
          ), name='password_reset_done'),
          
    # Enlace de Confirmación (Paso 3: Ingresar Nueva Contraseña)
    path('accounts/reset/<uidb64>/<token>/', 
          auth_views.PasswordResetConfirmView.as_view(
              template_name='password_reset_confirm.html',
              success_url='/accounts/reset/done/' 
          ), name='password_reset_confirm'),
          
    # Restablecimiento Completo (Paso 4: Finalizado)
    path('accounts/reset/done/', 
          auth_views.PasswordResetCompleteView.as_view(
              template_name='password_reset_complete.html' 
          ), name='password_reset_complete'),

    # 4. Rutas Específicas de Rol
    path('empresa/', include('empresas.urls')), # Prefijo para empresas
    path('aprendiz/', include('aprendices.urls')), # Prefijo para aprendices
    path('instructor/', include('instructores.urls')), # Prefijo para instructores
    path('gestion/', include('gestion.urls')), # Prefijo para administradores
    path('backups/', include('app_backups.urls')),


    # Si se necesitan archivos estáticos en desarrollo
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
