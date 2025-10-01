from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

# --- ADMIN ---

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

# --- INSTRUCTOR ---

@login_required
def dashboard_instructor(request):
    return render(request, 'instructores/dashboard.html')

@login_required
def gestionar_solicitudes(request):
    return HttpResponse("Página para gestionar solicitudes (Instructor)")

@login_required
def asignar_proyectos(request):
    return HttpResponse("Página para asignar proyectos (Instructor)")
