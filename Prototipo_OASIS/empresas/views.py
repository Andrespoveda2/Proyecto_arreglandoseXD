from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_empresa(request):
    """Renderiza el dashboard específico para el rol de Empresa."""
    return render(request, 'empresas/dashboard.html')

@login_required
def crear_proyecto(request):
    """Placeholder para la función de creación de proyecto."""
    return HttpResponse("Página para crear proyecto (Empresa)")

@login_required
def editar_proyecto(request, pk):
    """Placeholder para la función de edición de proyecto."""
    return HttpResponse(f"Página para editar proyecto con ID {pk} (Empresa)")

@login_required
def ver_solicitudes(request):
    """Placeholder para la función de ver solicitudes."""
    return HttpResponse("Página para ver solicitudes (Empresa)")
