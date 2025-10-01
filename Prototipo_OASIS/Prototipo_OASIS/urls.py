"""
URL configuration for Prototipo_OASIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Configuración del URL Resolver principal
urlpatterns = [
    # Admin nativo de Django, lo mantenemos separado
    path('superadmin/', admin.site.urls), 
    
    # 1. Rutas Públicas (App home) - Montada en la raíz
    path('', include('home.urls')),

    # 2. Rutas de Autenticación (App usuario) - Login, Registro, Perfil
    path('auth/', include('usuario.urls')),

    # 3. Rutas Específicas de Rol
    path('empresa/', include('empresas.urls')),
    path('aprendiz/', include('aprendices.urls')),
    path('instructor/', include('instructores.urls')),
    path('gestion/', include('gestion.urls')), # Gestión del superusuario

    # Si se necesitan archivos estáticos en desarrollo
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)