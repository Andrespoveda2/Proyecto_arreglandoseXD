from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_empresa(request):
    """Renderiza el dashboard específico para el rol de Empresa."""
    return render(request, 'empresas/dashboard.html')

def crear_proyecto(request):
    """Placeholder para la función de creación de proyecto."""
    return HttpResponse("Página para crear proyecto (Empresa)")

def ver_solicitudes(request):
    """Placeholder para la función de ver solicitudes."""
    return HttpResponse("Página para ver solicitudes (Empresa)")