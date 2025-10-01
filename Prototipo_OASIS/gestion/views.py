from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_gestion(request):
    """Renderiza el dashboard para el rol de Gestión/Administrador."""
    return render(request, 'gestion/dashboard.html')

@login_required
def gestionar_usuarios(request):
    """Herramientas para administrar usuarios y roles."""
    return HttpResponse("Página para gestionar usuarios (Gestión)")

@login_required
def proyectos_asignados(request):
    """Listado de proyectos que el admin o gestor supervisa."""
    return render(request, 'gestion/proyectos_asignados.html')

@login_required
def seguimiento_avance(request, pk):
    """Formulario para registrar avances o notas en proyecto."""
    return render(request, 'gestion/seguimiento_avance.html')
