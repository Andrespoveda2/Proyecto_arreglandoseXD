from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Función de test para asegurar que solo los admins accedan
def is_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN' and user.is_staff

@user_passes_test(is_admin)
def dashboard_admin(request):
    return render(request, 'admin/dashboard_admin.html')

@user_passes_test(is_admin)
def listar_usuarios(request):
    return render(request, 'admin/listar_usuarios.html')

@user_passes_test(is_admin)
def gestion_programas(request):
    return render(request, 'admin/gestion_programas.html')

@user_passes_test(is_admin)
def reportes(request):
    return render(request, 'admin/reportes.html')