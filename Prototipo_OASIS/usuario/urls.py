from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views # Importación necesaria para vistas de reset

# Importar el formulario corregido
from .forms import RestablecerContrasenaForm 


app_name = 'auth'

urlpatterns = [
    # 1. Rutas de Registro
    path('elegir/', views.elegir_registro, name='elegir_registro'),
    path('registro/aprendiz/', views.registro_aprendiz, name='registro_aprendiz'),
    path('registro/empresa/', views.registro_empresa, name='registro_empresa'),
    path('registro/instructor/', views.registro_instructor, name='registro_instructor'),

    # 2. Rutas de Autenticación (Login y Logout)
    path('login/', views.login_view, name='login'), 
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
    
    # 3. Otras Vistas
    path('contacto/', views.contacto_view, name='contacto'),
    path('manual_usuario/', views.manual_usuario, name='manual_usuario'),

    # 4. Rutas de restablecimiento de contraseña (AGREGADAS)
    
    # A. Solicitud de email
    path('reset_contrasena/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset_form.html',
        email_template_name='auth/password_reset_email.html',
        subject_template_name='auth/password_reset_subject.txt',
    ), name='password_reset'),

    # B. Email enviado
    path('reset_contrasena/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'
    ), name='password_reset_done'),

    # C. Ingresar nueva contraseña (Usa el formulario personalizado)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/password_reset_confirm.html',
        form_class=RestablecerContrasenaForm, 
    ), name='password_reset_confirm'),

    # D. Contraseña cambiada con éxito
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    #Manual de Usuario
    path('manual-usuario/', views.manual_usuario, name='manual_usuario'),
    path('manual-usuario/descargar/', views.descargar_manual_pdf, name='descargar_manual_pdf'),
]