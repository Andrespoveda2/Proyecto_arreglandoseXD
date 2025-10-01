from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_instructor(request):
    """Renderiza el dashboard específico para el rol de Instructor."""
    return render(request, 'instructores/dashboard.html')

def gestionar_solicitudes(request):
    """Placeholder para la función de gestión de solicitudes."""
    return HttpResponse("Página para gestionar solicitudes (Instructor)")

def asignar_proyectos(request):
    """Placeholder para la función de asignar proyectos."""
    return HttpResponse("Página para asignar proyectos (Instructor)")